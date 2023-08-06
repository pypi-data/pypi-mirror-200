# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pipen_cli_config']

package_data = \
{'': ['*'],
 'pipen_cli_config': ['frontend/*',
                      'frontend/assets/*',
                      'frontend/build/*',
                      'frontend/schema/*']}

install_requires = \
['pipen-annotate>=0.5,<0.6', 'pipen>=0.6,<0.7']

entry_points = \
{'pipen_cli': ['cli-config = pipen_cli_config:PipenCliConfigPlugin']}

setup_kwargs = {
    'name': 'pipen-cli-config',
    'version': '0.5.4',
    'description': 'UI wizard to generate configuration for pipen pipelines',
    'long_description': '# pipen-cli-config\n\nUI wizard to generate configuration for [pipen][1] pipelines\n\n## Install\n\n```shell\npip install -U pipen-cli-config\n```\n\n## Usage\n\n```shell\npipen config example_pipeline.py:pipeline\n```\n\n### Options\n\n```shell\n$ pipen config --help\nUsage: pipen config [-h] [--c-port C_PORT] [--c-additional C_ADDITIONAL] [--c-force]\n                    [--c-dev] [--c-noserve]\n                    pipeline\n\nCheck the requirements of a pipeline\n\nRequired Arguments:\n  pipeline              The pipeline and the CLI arguments to run the pipeline. For the\n                        pipeline either `/path/to/pipeline.py:<pipeline>` or\n                        `<module.submodule>:<pipeline>` `<pipeline>` must be an instance\n                        of `Pipen` and running the pipeline should be called under\n                        `__name__ == \'__main__\'.\n\nOptions:\n  -h, --help            show help message and exit\n  --c-port C_PORT       Port to serve the UI wizard [default: 18521]\n  --c-additional C_ADDITIONAL\n                        Additional arguments for the pipeline, in YAML, INI, JSON or TOML\n                        format\n  --c-force             Force re-generating the pipeline data. Note that previously saved\n                        data will be lost.\n  --c-dev               Run the pipeline in development mode. This will reload the\n                        pipeline module when it changes. Implies --c-force\n  --c-noserve           Do not serve the UI wizard, just generate the pipeline data file\n                        instead.\n                        Implies --c-force.\n                        [default: False]\n```\n\n### About additional arguments\n\nThe option `--c-additional` is used to pass additional arguments defined in a file to provide schemas for  `ADDITIONAL_OPTIONS` and `RUNNING_OPTIONS`. The file should be in YAML, INI, JSON or TOML format. The `ADDITIONAL_OPTIONS` are options that are not attached to the pipeline directly, but some "arbitrary" options that you can use in your pipeline, for example, to turn some processes on or off. The `RUNNING_OPTIONS` are options that are used to generate the running command of the pipeline.\n\nSee the example at `example/additiona.toml` for more details.\n\n## Example\n\nSee the example pipeline at `example/example.py` and the example UI at:\n\n[https://pwwang.github.io/pipen-cli-config/][2]\n\nNote that the saving function is not working in the example UI, because it is not served by `pipen-cli-config`.\n\n## Metadata of arguments\n\nIn your docstring, you can use the following metadata to describe the arguments:\n\n| Key | Description |\n| --- | --- |\n| `ctype` | The type of the argument |\n| `type` | Fallback to `ctype` if `ctype` is not provided |\n| `required` | Whether the argument is required |\n| `choices` | Implies `ctype="choice"` and will use subitems as choices |\n| `action=ns` | Implies `ctype="namespace"` and will use subitems as sub-arguments |\n| `mchoice(s)` | Implies `ctype="mchoice"` and will use subitems as choices |\n\nSupported types:\n\n| Type | Description |\n| --- | --- |\n| `bool` | Boolean |\n| `int` | Integer |\n| `float` | Float |\n| `str` | String |\n| `choice` | Choice |\n| `mchoice/mchoices` | Multiple choices |\n| `namespace/ns` | Namespace |\n| `text` | Text (multiple lines) |\n| `json` | Json |\n| `list/array` | List of items |\n| `auto` | Auto detect the type, in the order of `bool`, `None`, `int`, `float`, `json` and `str` |\n\n[1]: https://github.com/pwwang/pipen\n[2]: https://pwwang.github.io/pipen-cli-config/\n',
    'author': 'pwwang',
    'author_email': 'pwwang@pwwang.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
