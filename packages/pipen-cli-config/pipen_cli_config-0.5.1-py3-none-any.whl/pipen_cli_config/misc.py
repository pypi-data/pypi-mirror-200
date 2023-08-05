from __future__ import annotations

from typing import Any, Mapping, Type
from pathlib import Path
from tempfile import gettempdir
from urllib.parse import urlparse

from liquid import Liquid
from simpleconf import Config
from pipen import Proc
from pipen_annotate import annotate

from .defaults import PIPELINE_OPTIONS
from .utils import get_mark


def anno_to_argspec(
    anno: Mapping[str, Any] | None,
) -> Mapping[str, Any]:
    """Convert the annotation to the argument spec"""
    if anno is None:
        return {}

    argspec = {}
    # arginfo: attrs, help, terms
    for arg, arginfo in anno.items():
        argspec[arg] = arginfo.attrs.copy()
        # type - bool/text/choice/mchoice(s)/json/auto/list(array)/ns(namespace)
        # required
        # choices
        # itype
        if "ctype" not in argspec[arg]:
            if (argspec[arg].get("action") in ("store_true", "store_false")):
                argspec[arg]["type"] = "bool"
            elif (
                argspec[arg].get("action") in ("ns", "namespace")
                or argspec[arg].get("ns")
                or argspec[arg].get("namespace")
            ):
                argspec[arg]["type"] = "ns"
            elif (
                argspec[arg].get("action") in (
                    "append", "extend", "clear_append", "clear_extend"
                )
                or argspec[arg].get("array")
                or argspec[arg].get("list")
            ):
                argspec[arg]["type"] = "list"
            elif argspec[arg].get("choices") or argspec[arg].get("choice"):
                argspec[arg]["type"] = "choice"
            elif argspec[arg].get("mchoice") or argspec[arg].get("mchoices"):
                argspec[arg]["type"] = "mchoice"
        else:
            argspec[arg]["type"] = argspec[arg].pop("ctype")

        t = argspec[arg].get("type")
        if t == "ns":
            argspec[arg]["value"] = anno_to_argspec(arginfo.terms)
        elif t in ("choice", "mchoice"):
            argspec[arg]["value"] = argspec[arg].pop("default", [])
            argspec[arg]["choices"] = list(arginfo.terms)
            argspec[arg]["choices_desc"] = [
                term.help for term in arginfo.terms.values()
            ]
        else:
            argspec[arg]["value"] = argspec[arg].pop("default", None)

        # determine the itype for list elements
        if t == 'list':
            if (
                argspec[arg]["value"] is not None
                and not isinstance(argspec[arg]["value"], list)
            ):
                argspec[arg]["value"] = [argspec[arg]["value"]]
            if (
                argspec[arg]["value"] is not None
                and argspec[arg]["value"]
                and "itype" not in argspec[arg]
                and not isinstance(argspec[arg]["value"][0], str)
            ):
                argspec[arg]["itype"] = type(argspec[arg]["value"][0]).__name__

        argspec[arg]["desc"] = arginfo.help

    return argspec


def proc_to_argspec(
    proc: Proc | Type[Proc],
    is_start: bool,
) -> Mapping[str, Any]:
    """Convert the proc to the argument spec"""
    if isinstance(proc, Proc):
        anno = annotate(proc.__class__)
    else:
        anno = annotate(proc)

    summary = anno.get("Summary", {"short": "", "long": ""})
    argspec = {
        "is_start": is_start,
        "desc": f'# {summary["short"]}\n\n{summary["long"]}',
        "value": {},
    }
    if is_start and not get_mark(proc, "no_input"):
        argspec["value"]["in"] = {
            "desc": "The input data for the process",
            "type": "ns",
            "required": True,
            "value": anno_to_argspec(anno.get("Input", {})),
        }
    argspec["value"]["envs"] = {
        "desc": "Environment variables for the process, used across jobs",
        "value": anno_to_argspec(anno.get("Envs", {})),
    }
    argspec["value"]["plugin_opts"] = PIPELINE_OPTIONS["plugin_opts"]
    argspec["value"]["scheduler_opts"] = PIPELINE_OPTIONS["scheduler_opts"]
    argspec["value"]["forks"] = PIPELINE_OPTIONS["forks"]
    argspec["value"]["cache"] = PIPELINE_OPTIONS["cache"]
    argspec["value"]["scheduler"] = PIPELINE_OPTIONS["scheduler"]
    argspec["value"]["dirsig"] = PIPELINE_OPTIONS["dirsig"]
    argspec["value"]["error_strategy"] = PIPELINE_OPTIONS["error_strategy"]
    argspec["value"]["num_retries"] = PIPELINE_OPTIONS["num_retries"]
    argspec["value"]["lang"] = {
        "desc": "The interpreter to run the script",
        "hidden": True,
        "placeholder": proc.lang,
        # Don't include it in the config file if not specified
        "value": None,
    }

    return argspec


def load_additional(additional: str, **kwargs) -> Mapping[str, Any]:
    """Load additional config files"""
    if not additional:
        return {}

    parsed = urlparse(additional)
    cache_dir = Path(gettempdir()) / 'pipen-cli-config-additional-configs'
    cache_dir.mkdir(parents=True, exist_ok=True)
    if parsed.scheme in ('http', 'https', 'ftp', 'ftps', 'gh'):
        from hashlib import sha256
        from urllib.error import URLError
        from urllib.request import urlretrieve

        if parsed.scheme == 'gh':
            try:
                user, repo, file_path = parsed.path.split('/', 2)
            except ValueError:
                raise ValueError(f"Invalid gh:// URL: {additional}")
            branch = 'master'
            if '@' in file_path:
                file_path, branch = file_path.split('@')
            parsed = urlparse(
                "https://raw.githubusercontent.com/"
                f"{user}/{repo}/{branch}/{file_path}"
            )

        url = parsed.geturl()
        cache_key = sha256(url.encode('utf-8')).hexdigest()
        additional = cache_dir / f"{cache_key}-{parsed.path.split('/')[-1]}"
        if not additional.exists():
            try:
                urlretrieve(url, additional)
            except URLError:
                raise ValueError(
                    f"Could not retrieve remote path: {additional}"
                ) from None

    if not kwargs:
        return Config.load(additional)

    # kwargs passed, treat the file as a template
    additional = Path(additional)
    tpl = Liquid(additional, mode="wild", from_file=True)
    configfile = cache_dir / f"{additional.stem}.rendered{additional.suffix}"
    Path("x.log").write_text(str(kwargs))
    configfile.write_text(tpl.render(**kwargs))
    return Config.load(configfile)
