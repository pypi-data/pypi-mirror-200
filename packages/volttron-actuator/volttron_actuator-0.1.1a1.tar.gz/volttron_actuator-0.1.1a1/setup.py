# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['actuator']

package_data = \
{'': ['*']}

install_requires = \
['types-tzlocal>=4.2.2.2,<5.0.0.0',
 'tzlocal>=4.2,<5.0',
 'volttron>=10.0.2rc0,<11.0']

entry_points = \
{'console_scripts': ['volttron-actuator = actuator.agent:main']}

setup_kwargs = {
    'name': 'volttron-actuator',
    'version': '0.1.1a1',
    'description': 'The Actuator Agent is used to manage write access to devices. Other agents may request scheduled times, called Tasks, to interact with one or more devices.',
    'long_description': '# volttron-actuator\n\n[![Passing?](https://github.com/VOLTTRON/volttron-actuator/actions/workflows/run-tests.yml/badge.svg)](https://github.com/VOLTTRON/volttron-actuator/actions/workflows/run-tests.yml)\n[![pypi version](https://img.shields.io/pypi/v/volttron-actuator.svg)](https://pypi.org/project/volttron-actuator/)\n\n\nThe Actuator Agent is used to manage write access to devices. Other agents may request scheduled times, called Tasks, to interact with one or more devices.\n\n## Prerequisites\n\n* Python 3.8\n\n## Python\n\n<details>\n<summary>To install Python 3.8, we recommend using <a href="https://github.com/pyenv/pyenv"><code>pyenv</code></a>.</summary>\n\n```bash\n# install pyenv\ngit clone https://github.com/pyenv/pyenv ~/.pyenv\n\n# setup pyenv (you should also put these three lines in .bashrc or similar)\nexport PATH="${HOME}/.pyenv/bin:${PATH}"\nexport PYENV_ROOT="${HOME}/.pyenv"\neval "$(pyenv init -)"\n\n# install Python 3.8\npyenv install 3.8.10\n\n# make it available globally\npyenv global system 3.8.10\n```\n</details>\n\n# Installation\n\nCreate and activate a virtual environment.\n\n```shell\npython -m venv env\nsource env/bin/activate\n```\n\nInstalling volttron-platform-driver requires a running volttron instance.\n\n```shell\npip install volttron\n\n# Start platform with output going to volttron.log\nvolttron -vv -l volttron.log &\n```\n\nInstall and start the volttron-actuator.\n\n```shell\nvctl install volttron-actuator --agent-config <path to agent config> --start\n```\n\nView the status of the installed agent\n\n```shell\nvctl status\n```\n\n# Development\n\nPlease see the following for contributing guidelines [contributing](https://github.com/eclipse-volttron/volttron-core/blob/develop/CONTRIBUTING.md).\n\nPlease see the following helpful guide about [developing modular VOLTTRON agents](https://github.com/eclipse-volttron/volttron-core/blob/develop/DEVELOPING_ON_MODULAR.md)\n\n\n# Disclaimer Notice\n\nThis material was prepared as an account of work sponsored by an agency of the\nUnited States Government.  Neither the United States Government nor the United\nStates Department of Energy, nor Battelle, nor any of their employees, nor any\njurisdiction or organization that has cooperated in the development of these\nmaterials, makes any warranty, express or implied, or assumes any legal\nliability or responsibility for the accuracy, completeness, or usefulness or any\ninformation, apparatus, product, software, or process disclosed, or represents\nthat its use would not infringe privately owned rights.\n\nReference herein to any specific commercial product, process, or service by\ntrade name, trademark, manufacturer, or otherwise does not necessarily\nconstitute or imply its endorsement, recommendation, or favoring by the United\nStates Government or any agency thereof, or Battelle Memorial Institute. The\nviews and opinions of authors expressed herein do not necessarily state or\nreflect those of the United States Government or any agency thereof.\n',
    'author': 'Mark Bonicillo',
    'author_email': 'volttron@pnnl.gov',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/VOLTTRON/volttron-actuator',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
