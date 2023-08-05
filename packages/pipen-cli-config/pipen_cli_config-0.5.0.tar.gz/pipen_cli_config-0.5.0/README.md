# pipen-cli-config

UI wizard to generate configuration for [pipen][1] pipelines

## Install

```shell
pip install -U pipen-cli-config
```

## Usage

```shell
pipen config example_pipeline.py:pipeline
```

### Options

```shell
$ pipen config --help
Usage: pipen config [-h] [--c-port C_PORT] [--c-additional C_ADDITIONAL] [--c-force]
                    [--c-dev] [--c-noserve]
                    pipeline

Check the requirements of a pipeline

Required Arguments:
  pipeline              The pipeline and the CLI arguments to run the pipeline. For the
                        pipeline either `/path/to/pipeline.py:<pipeline>` or
                        `<module.submodule>:<pipeline>` `<pipeline>` must be an instance
                        of `Pipen` and running the pipeline should be called under
                        `__name__ == '__main__'.

Options:
  -h, --help            show help message and exit
  --c-port C_PORT       Port to serve the UI wizard [default: 18521]
  --c-additional C_ADDITIONAL
                        Additional arguments for the pipeline, in YAML, INI, JSON or TOML
                        format
  --c-force             Force re-generating the pipeline data. Note that previously saved
                        data will be lost.
  --c-dev               Run the pipeline in development mode. This will reload the
                        pipeline module when it changes. Implies --c-force
  --c-noserve           Do not serve the UI wizard, just generate the pipeline data file
                        instead.
                        Implies --c-force.
                        [default: False]
```

### About additional arguments

The option `--c-additional` is used to pass additional arguments defined in a file to provide schemas for  `ADDITIONAL_OPTIONS` and `RUNNING_OPTIONS`. The file should be in YAML, INI, JSON or TOML format. The `ADDITIONAL_OPTIONS` are options that are not attached to the pipeline directly, but some "arbitrary" options that you can use in your pipeline, for example, to turn some processes on or off. The `RUNNING_OPTIONS` are options that are used to generate the running command of the pipeline.

See the example at `example/additiona.toml` for more details.

## Example

See the example pipeline at `example/example.py` and the example UI at:

[https://pwwang.github.io/pipen-cli-config/][2]

Note that the saving function is not working in the example UI, because it is not served by `pipen-cli-config`.

## Metadata of arguments

In your docstring, you can use the following metadata to describe the arguments:

| Key | Description |
| --- | --- |
| `ctype` | The type of the argument |
| `type` | Fallback to `ctype` if `ctype` is not provided |
| `required` | Whether the argument is required |
| `choices` | Implies `ctype="choice"` and will use subitems as choices |
| `action=ns` | Implies `ctype="namespace"` and will use subitems as sub-arguments |
| `mchoice(s)` | Implies `ctype="mchoice"` and will use subitems as choices |

Supported types:

| Type | Description |
| --- | --- |
| `bool` | Boolean |
| `int` | Integer |
| `float` | Float |
| `str` | String |
| `choice` | Choice |
| `mchoice/mchoices` | Multiple choices |
| `namespace/ns` | Namespace |
| `text` | Text (multiple lines) |
| `json` | Json |
| `list/array` | List of items |
| `auto` | Auto detect the type, in the order of `bool`, `None`, `int`, `float`, `json` and `str` |

[1]: https://github.com/pwwang/pipen
[2]: https://pwwang.github.io/pipen-cli-config/
