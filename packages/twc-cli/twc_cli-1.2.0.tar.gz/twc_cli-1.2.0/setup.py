# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['twc', 'twc.api', 'twc.commands']

package_data = \
{'': ['*']}

install_requires = \
['click-aliases>=1.0.1,<2.0.0',
 'click>=8.1.3,<9.0.0',
 'pygments>=2.14.0,<3.0.0',
 'pyyaml>=6.0,<7.0',
 'requests>=2.28.1,<3.0.0',
 'toml>=0.10.2,<0.11.0']

entry_points = \
{'console_scripts': ['twc = twc.__main__:cli']}

setup_kwargs = {
    'name': 'twc-cli',
    'version': '1.2.0',
    'description': 'Timeweb Cloud Command Line Interface.',
    'long_description': '![TWC CLI](https://github.com/timeweb-cloud/twc/blob/master/artwork/logo.svg)\n\nTimeweb Cloud Command Line Interface and simple SDK 💫\n\n> [Документация на русском](https://github.com/timeweb-cloud/twc/blob/master/docs/ru/README.md) 🇷🇺\n\n# Installation\n\n```\npip install twc-cli\n```\n\n# Getting started\n\nGet Timeweb Cloud [access token](https://timeweb.cloud/my/api-keys) and\nconfigure **twc** with command:\n\n```\ntwc config\n```\n\nEnter your access token and hit `Enter`.\n\nConfiguration done! Let\'s use:\n\n```\ntwc --help\n```\n\n# Shell completion\n\n## Bash\n\nAdd this to **~/.bashrc**:\n\n```\neval "$(_TWC_COMPLETE=bash_source twc)"\n```\n\n## Zsh\n\nAdd this to **~/.zshrc**:\n\n```\neval "$(_TWC_COMPLETE=zsh_source twc)"\n```\n\n## Fish\n\nAdd this to **~/.config/fish/completions/tw.fish**:\n\n```\neval (env _TWC_COMPLETE=fish_source twc)\n```\n',
    'author': 'ge',
    'author_email': 'dev@timeweb.cloud',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/timeweb-cloud/twc',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.9,<4.0.0',
}


setup(**setup_kwargs)
