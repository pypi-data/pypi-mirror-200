# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['gptroles',
 'gptroles.ui',
 'gptroles.ui.widgets',
 'gptroles.ui.widgets.terminal']

package_data = \
{'': ['*'],
 'gptroles.ui': ['web/*', 'web/dist/*', 'web/src/*', 'web/src/static/*']}

install_requires = \
['appdirs>=1.4.4,<2.0.0',
 'langchain>=0.0.126,<0.0.127',
 'openai>=0.27.2',
 'pydantic>=1.10.7,<2.0.0',
 'pygments>=2.14.0,<3.0.0',
 'pyqt6-webengine>=6.4.0',
 'pyqt6>=6.4.2',
 'toml>=0.10.2,<0.11.0']

entry_points = \
{'console_scripts': ['devtest = mypackage:test.run_tests',
                     'main = gptroles.main:main']}

setup_kwargs = {
    'name': 'gptroles',
    'version': '0.1.3',
    'description': 'Interact with chatgpt and assign different roles',
    'long_description': '\n## GPT Roles\nSimple PyQT chatbox that connects to a chat session with ChatGPT, along with some extra desktop integration features.\n\nWritten as an experiment with Qt and understanding the role of LLMs in virtual assistant applications.\n\n![Screenshot of GPT Roles](doc/screenshot.png)\n![Demo video of GPT Roles](doc/demo.webm)\n\n#### Roleplayer\nIt has a "roleplaying" root prompt that attempts to make implementing more roles into ChatGPT easier.\nYou can add "roles" to the root prompt, by default there are some roles related to commands and programming.\n\nYou can also change the root prompt to something else entirely, there\'s a list of some prompts that are sourced online, see features.\n\n###### Command Role\n\nNot fully implemented\n\n    - RoleGPT can request web pages or from APIs to answer your questions.\n        e.g. get current prices or latest news.\n    - Provide basic shell commands that will be automatically be run, to find or list files etc\n    - Instructions to format markdown for the programming features\n\n#### App Features\n\nProgramming related features:\n\n    - Run shell or python code in markdown blocks directly in the chat interface\n    - Edit the markdown blocks in the chat box\n    - Copy or save markdown blocks to a file\n\nAdditional features:\n\n    - Easily switch or add more "roles"\n    - Remove the roleplaying root prompt and set it as you please\n    - List roles from jailbreakchat.com and set them as the root prompt\n\nChat related features:\n\n    - TODO Shows which messages are in the current prompt chain and can be added/removed\n    - TODO Show alternate choices and commit to conversation\n\n\n#### Installing/Running\n\n###### From pip\nInstall the module and install desktop launcher integration:\n\n`pip install gptroles && ./install.sh`\n\n\n###### From source with Poetry\n```shell\npoetry install && poetry run main\n```\n\n###### Packaged AppImage/PyInstaller\n\n`TODO`\n\n###### Development installation\n\nUse the `dev.sh` script.\n\n```shell\n# This only needs to be run once\n./dev.sh build && ./dev.sh sysinstall && ./dev.sh install\n\n# Then you can run with the install and dev environment matching code\n./dev.sh run\n```',
    'author': 'Blipk A.D.',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/blipk/gptroles',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
