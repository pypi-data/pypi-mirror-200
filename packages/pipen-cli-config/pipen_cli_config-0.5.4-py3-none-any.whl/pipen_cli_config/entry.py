"""Provides PipenCliRequire"""
from __future__ import annotations

import asyncio
import importlib
import importlib.util
import http.server
import itertools
import json
import socketserver
import sys
from pathlib import Path
from typing import TYPE_CHECKING, Any, Mapping

from slugify import slugify
from pipen import Pipen, ProcGroup
from pipen.utils import get_logger
from pipen.cli import CLIPlugin
from pipen_annotate import annotate

from .defaults import (
    PIPEN_CLI_CONFIG_DIR,
    PIPELINE_OPTIONS,
    SECTION_PIPELINE_OPTIONS,
    SECTION_PROCGROUPS,
    SECTION_PROCESSES,
)
from .misc import anno_to_argspec, proc_to_argspec, load_additional
from .utils import get_mark
from .version import __version__

if TYPE_CHECKING:  # pragma: no cover
    from argx import ArgumentParser, Namespace

logger = get_logger("config")


class PipenCliConfigPlugin(CLIPlugin):
    """Check the requirements of a pipeline"""

    version = __version__
    name = "config"

    def __init__(
        self,
        parser: ArgumentParser,
        subparser: ArgumentParser,
    ) -> None:
        super().__init__(parser, subparser)
        subparser.add_argument(
            "--c-port",
            type=int,
            default=18521,
            dest="c_port",
            help="Port to serve the UI wizard",
        )
        subparser.add_argument(
            "--c-additional",
            dest="c_additional",
            help=(
                "Additional arguments for the pipeline, "
                "in YAML, INI, JSON or TOML format"
            ),
        )
        subparser.add_argument(
            "--c-force",
            action="store_true",
            dest="c_force",
            help=(
                "Force re-generating the pipeline data. "
                "Note that previously saved data will be lost."
            ),
        )
        subparser.add_argument(
            "--c-dev",
            action="store_true",
            dest="c_dev",
            help=(
                "Run the pipeline in development mode. "
                "This will reload the pipeline module when it changes. "
                "Implies --c-force"
            ),
        )
        subparser.add_argument(
            "--c-loglevel",
            dest="c_loglevel",
            help=(
                "Logging level. If `auto`, "
                "set to `debug` if `--c-dev` is set, otherwise `info`"
            ),
            choices=("auto", "debug", "info", "warning", "error", "critical"),
            default="auto",
        )
        subparser.add_argument(
            "--c-noserve",
            action="store_true",
            dest="c_noserve",
            help=(
                "Do not serve the UI wizard, "
                "just generate the pipeline data file instead.\n"
                "Implies --c-force."
            ),
            default=False,
        )
        subparser.add_argument(
            "pipeline",
            help=(
                "The pipeline and the CLI arguments to run the pipeline. "
                "For the pipeline either `/path/to/pipeline.py:<pipeline>` "
                "or `<module.submodule>:<pipeline>` "
                "`<pipeline>` must be an instance of `Pipen` and running "
                "the pipeline should be called under `__name__ == '__main__'."
            ),
        )

    def parse_args(self) -> Namespace:
        parsed, rest = self.parser.parse_known_args(fromfile_keep=True)
        parsed.pipeline_args = rest
        return parsed

    def _parse_pipeline(self, pipeline: str) -> Pipen:
        """Parse the pipeline"""
        modpath, sep, name = pipeline.rpartition(":")
        if sep != ":":
            raise ValueError(
                f"Invalid pipeline: {pipeline}.\n"
                "It must be in the format '<module[.submodule]>:pipeline' or \n"
                "'/path/to/pipeline.py:pipeline'"
            )

        path = Path(modpath)
        if path.is_file():
            spec = importlib.util.spec_from_file_location(path.stem, modpath)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
        else:
            module = importlib.import_module(modpath)

        try:
            pipeline = getattr(module, name)
        except AttributeError:
            raise ValueError(f"Invalid pipeline: {pipeline}") from None

        if isinstance(pipeline, type) and issubclass(pipeline, Pipen):
            pipeline = pipeline()

        if isinstance(pipeline, type) and issubclass(pipeline, ProcGroup):
            pipeline = pipeline().as_pipen()

        if not isinstance(pipeline, Pipen):
            raise ValueError(
                f"Invalid pipeline: {pipeline}\n"
                "It must be a `pipen.Pipen` instance"
            )

        return pipeline

    async def _get_pipeline_data(self, args: Namespace) -> Mapping[str, Any]:
        """Get the pipeline data"""
        cached_file = PIPEN_CLI_CONFIG_DIR / f"{slugify(args.pipeline)}.json"
        if not args.c_force and cached_file.exists():
            logger.warning(f"Loading pipeline data from {cached_file}")
            logger.warning(
                "Remove the file to force re-generating the pipeline data"
            )
            logger.warning(
                "Or use `--c-force` to force re-generating the pipeline data"
            )
            with cached_file.open() as f:
                return json.load(f)

        if args.c_force:
            logger.warning("You are forcing re-generating the pipeline data.")
            logger.warning("Previously saved data will NOT be loaded.")

        if cached_file.exists():
            from datetime import datetime

            now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            bakfile = cached_file.with_suffix(f".json.{now}")
            cached_file.rename(bakfile)
            logger.warning(f"Moved previously saved data to {bakfile}")

        old_argv = sys.argv
        sys.argv = ["from-pipen-cli-config"] + args.pipeline_args
        logger.info("Fetching pipeline data ...")
        try:
            pipeline = self._parse_pipeline(args.pipeline)
            # Initialize the pipeline so that the arguments definied by
            # other plugins (i.e. pipen-args) to take in place.
            await pipeline._init()
            pipeline.build_proc_relationships()
        finally:
            sys.argv = old_argv

        if args.c_additional:
            logger.info("Loading additional configuration items ...")
            data = load_additional(
                args.c_additional,
                pipeline=args.pipeline,
                pipeline_args=args.pipeline_args,
            )
        else:
            data = {}

        data[SECTION_PIPELINE_OPTIONS] = PIPELINE_OPTIONS
        data[SECTION_PIPELINE_OPTIONS]["name"] = {
            "type": "str",
            "value": pipeline.name,
            "placeholder": pipeline.name,
            # used for saving
            "cached_file": cached_file.name,
            "desc": (
                "The name of the pipeline. "
                "It will affect the names of working directory and "
                "the result directory"
            ),
        }
        data[SECTION_PIPELINE_OPTIONS]["desc"] = {
            "type": "str",
            "value": pipeline.desc,
            "desc": (
                "The description of the pipeline, "
                "shows in the log and report."
            ),
        }
        data[SECTION_PIPELINE_OPTIONS]["outdir"] = {
            "desc": "The output directory of your pipeline",
            "placeholder": "./<name>_results",
            "type": "str",
            "value": None,
        }
        data[SECTION_PROCESSES] = {}
        data[SECTION_PROCGROUPS] = {}
        for proc in pipeline.procs:
            logger.debug("Parsing process %s ..." % proc.name)
            if get_mark(proc, "hidden"):
                continue
            if proc.__procgroup__:
                if proc.__procgroup__.name not in data[SECTION_PROCGROUPS]:
                    data[SECTION_PROCGROUPS][proc.__procgroup__.name] = {
                        "PROCESSES": {}
                    }
                    pg_args = anno_to_argspec(
                        annotate(proc.__procgroup__.__class__).get(
                            "Args", None
                        )
                    )
                    if pg_args:
                        for arg, arginfo in pg_args.items():
                            arginfo["value"] = proc.__procgroup__.DEFAULTS.get(
                                arg
                            )
                        data[SECTION_PROCGROUPS][proc.__procgroup__.name][
                            "ARGUMENTS"
                        ] = pg_args

                data[SECTION_PROCGROUPS][proc.__procgroup__.name][
                    SECTION_PROCESSES
                ][proc.name] = proc_to_argspec(proc, proc in pipeline.starts)
            else:
                data[SECTION_PROCESSES][proc.name] = proc_to_argspec(
                    proc,
                    proc in pipeline.starts,
                )

        logger.info("Saving data to %s ..." % cached_file)
        cached_file.parent.mkdir(parents=True, exist_ok=True)
        with cached_file.open("w") as f:
            json.dump(data, f, indent=2)
        return data

    def exec_command(self, args: Namespace) -> None:
        """Execute the command"""
        if args.c_loglevel == "auto":
            args.c_loglevel = "debug" if args.c_dev else "info"
        logger.setLevel(args.c_loglevel.upper())

        logger.info(
            "[bold]pipen-cli-config: [/bold]"
            "UI wizard to generate configuration for pipen pipelines"
        )
        logger.info(f"[bold]version: [/bold]{__version__}")
        logger.info("")

        if args.c_noserve:
            logger.info("Not serving the UI")
            args.c_force = True
            data = asyncio.run(self._get_pipeline_data(args))
            cached_file = PIPEN_CLI_CONFIG_DIR.joinpath(
                data["PIPELINE_OPTIONS"]["name"]["cached_file"]
            )
            logger.info(f"Pipeline data saved to {cached_file}")
            return

        # Avoid data to be loaded twice in do_GET in the same session
        loaded_data = None

        class HTTPHandler(http.server.SimpleHTTPRequestHandler):
            # python 3.9 doesn't have this
            _control_char_table = str.maketrans(
                {
                    c: rf"\x{c:02x}"
                    for c in itertools.chain(range(0x20), range(0x7F, 0xA0))
                }
            )
            _control_char_table[ord("\\")] = r"\\"

            def __init__(this, *args, **kwargs):
                path = Path(__file__).parent / "frontend"
                super().__init__(*args, directory=path, **kwargs)

            def do_GET(this):
                if this.path == "/schema/pipeline.json":
                    if not args.c_dev:
                        nonlocal loaded_data
                        if loaded_data is None:
                            loaded_data = json.dumps(
                                asyncio.run(self._get_pipeline_data(args))
                            ).encode("utf-8")
                        this.send_response(200)
                        this.send_header("Content-type", "application/json")
                        this.end_headers()
                        this.wfile.write(loaded_data)
                    else:
                        from multiprocessing import Process, Pipe

                        args.c_force = True
                        # Use multiprocessing to get a clean environment
                        # to load the pipeline to avoid conflicts
                        def target(conn):
                            conn.send(
                                json.dumps(
                                    asyncio.run(
                                        self._get_pipeline_data(args)
                                    )
                                ).encode("utf-8")
                            )
                            conn.close()

                        parent_conn, child_conn = Pipe()
                        p = Process(target=target, args=(child_conn,))
                        p.start()
                        ldata = parent_conn.recv()
                        p.join()
                        this.send_response(200)
                        this.send_header("Content-type", "application/json")
                        this.end_headers()
                        this.wfile.write(ldata)
                else:
                    try:
                        super().do_GET()
                    except BrokenPipeError:
                        pass

            def do_POST(this):
                if this.path == "/save":
                    if not loaded_data:
                        logger.warning(
                            "Skipping saving pipeline data, "
                            "since it's not loaded yet. "
                            "Please reload the page and try again."
                        )
                        return

                    this.send_response(200)
                    this.send_header("Content-type", "application/json")
                    this.end_headers()
                    data = json.loads(
                        this.rfile.read(
                            int(this.headers["Content-Length"])
                        ).decode("utf-8")
                    )
                    cached_file = PIPEN_CLI_CONFIG_DIR.joinpath(
                        data["PIPELINE_OPTIONS"]["name"]["cached_file"]
                    )
                    with cached_file.open("w") as f:
                        json.dump(data, f, indent=2)
                    logger.info("Saved pipeline data to %s", cached_file)
                else:
                    super().do_POST()

            def log_message(this, format: str, *args: Any) -> None:
                message = format % args
                message = (
                    f"[{this.address_string()}] "
                    f"{message.translate(this._control_char_table)}"
                )
                logger.info(message)

        port = getattr(args, "c-port", 0)

        socketserver.TCPServer.allow_reuse_address = True
        with socketserver.TCPServer(("", args.c_port), HTTPHandler) as httpd:
            port = httpd.server_address[1]
            url = f"Serving UI wizard at http://localhost:{port}"
            logger.info(f"{url}?dev=1" if args.c_dev else url)
            logger.info("Press Ctrl+C to exit")
            logger.info("")
            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                logger.error("Stopping the server")
