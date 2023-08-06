# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['__init__', 'py']
install_requires = \
['colorama>=0.4.4,<0.5.0']

setup_kwargs = {
    'name': 'chromaformatter',
    'version': '6.0.0',
    'description': 'Wrapper for the Python logging formatter that adds color.',
    'long_description': '<div align="center">\n<!-- Title: -->\n  <h1>Chroma Formatter</h1>\n<!-- Labels: -->\n  <!-- First row: -->\n  <img src="https://img.shields.io/badge/license-MIT-green"\n   height="20"\n   alt="License: MIT">\n  <img src="https://img.shields.io/badge/code%20style-black-000000.svg"\n   height="20"\n   alt="Code style: black">\n  <img src="https://img.shields.io/pypi/v/chromaformatter.svg"\n   height="20"\n   alt="PyPI version">\n  <img src="https://img.shields.io/badge/coverage-100%25-success"\n   height="20"\n   alt="Code Coverage">\n  <h3>Wrapper for Python logging formatter that adds color</h3>\n  <img src="https://gitlab.com/mburkard/chroma-formatter/-/raw/main/docs/chroma_demo.png"\n   alt="Demo">\n</div>\n\n## Installation\n\nChroma Formatter is on PyPI and can be installed with:\n\n```\npip install chromaformatter\n```\n\n## Usage\n\nChroma Formatter adds two features to the default logging formatter, colors can be added\nto the log format string, and formatted arguments in a log message can be colored.\nColors can be inserted info the format string as such:\n\n```python\nlog_format = (\n    f\'{Colors.Fore.GREEN}%(asctime)-s \'\n    f\'{Colors.LEVEL_COLOR}%(levelname).1s \'\n    f\'{Colors.Fore.MAGENTA}%(filename)-s:%(lineno)03d \'\n    f\'{Colors.LEVEL_COLOR}- %(message)s\'\n)\n```\n\nThen, use chromaformatter.ChromaFormatter rather than logging.Formatter.\n\n```python\nimport sys\nimport logging\n\nfrom chromaformatter import ChromaFormatter, Colors\n\nlog = logging.getLogger()\nlog_format = (\n    f\'{Colors.Fore.GREEN}%(asctime)-s \'\n    f\'{Colors.LEVEL_COLOR}%(levelname).1s \'\n    f\'{Colors.Fore.MAGENTA}%(filename)-s:%(lineno)03d \'\n    f\'{Colors.LEVEL_COLOR}- %(message)s\'\n)\nformatter = ChromaFormatter(\n    fmt=log_format,\n    arg_start_color=Colors.Fore.WHITE,\n    arg_end_color=Colors.LEVEL_COLOR\n)\nhandler = logging.StreamHandler(stream=sys.stdout)\nhandler.setFormatter(formatter)\nlog.addHandler(handler)\n```\n\n### Formatted Arguments in a Log\n\nBy setting `arg_start_color` for argument colors and `arg_end_color` for the rest of the\nstring that comes after the argument, those colors will be applied to arguments.\n\n```python\nlog.info(\'This %s will be colored.\', \'variable\')\n```\n\n### Additional Configuration\n\nChromaFormatter has a dict called `color_map` to determine the colors of each logging\nlevel.\n\nBy default, the colors are:\n\n| Category | Color             |\n|----------|-------------------|\n| NOTSET   | Fore.LIGHTBLUE_EX |\n| DEBUG    | Fore.BLUE         |\n| INFO     | Fore.Cyan         |\n| WARNING  | Fore.YELLOW       |\n| ERROR    | Fore.LIGHTRED_EX  |\n| CRITICAL | Fore.RED          |\n| ARGS     | Fore.White        |\n\nColor map can be changed as such:\n\n```python\nformatter.color_map[logging.INFO] = Colors.Fore.WHITE\nformatter.color_map[logging.DEBUG] = Colors.Fore.MAGENTA\n```\n\n## Applying to Existing Loggers\n\nIf you are using a third party module that uses the standard python logging module you\ncan apply a ChromaFormatter as such:\n\n```python\nimport sys\nimport logging\n\nfrom chromaformatter import ChromaFormatter, Colors\n\nlog_format = (\n    f\'{Colors.Fore.GREEN}%(asctime)-s \'\n    f\'{Colors.LEVEL_COLOR}%(levelname).1s \'\n    f\'{Colors.Fore.MAGENTA}%(filename)-s:%(lineno)03d \'\n    f\'{Colors.LEVEL_COLOR}- %(message)s\'\n)\nstream_formatter = ChromaFormatter(log_format)\nstream_handler = logging.StreamHandler(stream=sys.stdout)\n\nflask_logger = logging.getLogger(\'werkzeug\')\nwhile flask_logger.handlers:\n    flask_logger.removeHandler(flask_logger.handlers.pop())\nflask_logger.addHandler(stream_handler)\n```\n',
    'author': 'Matthew Burkard',
    'author_email': 'matthewjburkard@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/mburkard/chroma-formatter',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
