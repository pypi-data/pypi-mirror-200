# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['terminal_translator']

package_data = \
{'': ['*']}

install_requires = \
['dynaconf>=3.1.12,<4.0.0',
 'google-cloud-translate>=3.11.0,<4.0.0',
 'pyperclip>=1.8.2,<2.0.0',
 'rich>=13.3.2,<14.0.0',
 'toml>=0.10.2,<0.11.0',
 'typer>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['tt = terminal_translator.main:app',
                     'tt-configure = terminal_translator.config:app_config']}

setup_kwargs = {
    'name': 'tt-terminal-translator',
    'version': '0.1.0',
    'description': 'Terminal Translator is a translation CLI that uses the Google Cloud API. ',
    'long_description': '# Terminal Translator \n[![Documentation Status](https://readthedocs.org/projects/terminal-translator/badge/?version=latest)](https://terminal-translator.readthedocs.io/en/latest/?badge=latest)\n\nTerminal Translator is a translation CLI that uses the [Google Cloud API](https://cloud.google.com/translate).\n\n## Documentation\n\nSee the [full documentation](https://terminal-translator.readthedocs.io/en/latest/)\n\n## Installation\n\nInstallation is very simple, just run the following command in the terminal:\n\n```bash\npip install tt-terminal-translator\n```\n\n## Basic Usage\n\nThe CLI consists of two commands, `tt` and `tt-configure`.\n\n### tt\n\n`tt` is the main CLI command.\n\n**Usage**\n\nBasically we call the command passing the text to be translated\n\nBy default the text will be translated to `en-us`\n\n```bash\ntt ola mundo\n```\n![tt](./docs/assets/images/tt.png)\n\nWe can also inform the target language for the translation\n\n```bash\ntt ola mundo --target es  # spanish\n```\n![tt-2](./docs/assets/images/tt-2.png)\n\nThere is also a parameter to translate directly into Portuguese\n\n```bash\ntt hello world -p\n```\n![tt-3](./docs/assets/images/tt-3.png)\n\n\nIn addition there is a parameter to copy the output directly to the clipboard\n\n```bash\ntt -c hola mundo\n```\n![tt-4](./docs/assets/images/tt-4.png)\n\nFor more information use the parameter `--help`\n\n```bash\ntt --help\n```\n\n![tt-5](./docs/assets/images/tt-5.png)\n\n\n\n### tt-configure\n\n`tt-configure` is only for the initial configuration of the Google Cloud API credentials, as seen in the [settings section](/#configuration).\n\n**Usage**\n\nBasically we call the command passing two arguments, first the project-id followed by the path of the credentials Json file.\n\n```bash\ntt-configure <project-id> <google-api-credentials>\n```\n\nFor quick help use the `--help` argument.\n\n\n```bash\ntt-configure --help\n```\n![tt-configure](./docs/assets/images/tt-configure.png)\n\n',
    'author': 'gbPagano',
    'author_email': 'guilhermebpagano@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
