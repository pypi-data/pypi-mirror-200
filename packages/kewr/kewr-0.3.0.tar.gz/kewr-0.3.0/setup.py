# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kewr']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0', 'confection>=0.0.4,<0.0.5']

setup_kwargs = {
    'name': 'kewr',
    'version': '0.3.0',
    'description': 'A simple python script manager',
    'long_description': '# KEWR\n\nA simple python script runner.\n\nMany processes we use python for consist of a set of scripts, with particular inputs and outputs. tskr can be used to track all the scripts in a workflow and run them independently. \n\nFor example, our project might include scripts to preprocess some data, do some analysis, then produce some plots. Each of these scripts might take arguments or options. We might complete the sequence like this \n\n```\npython ./preprocess_script.py /path/to/data\npython ./analysis_script.py argument_1 --optional-flag  \npython ./plotting_script.py /path/to/plot/dir\n```\n\ntskr aims to keep our scripts organized along with their arguments.\n\n## Installation\n\n```\npip install kewr\n```\n\n## Usage\n\nFirst create a new config file\n\n```\npython -m kewr create #creates a new tskr config file in the directory\n```\n\nIn this file we define the stages of our script sequence. The config is a .toml file with sections for each stage.\n\n```\n[stage1]\nhelp = "description of what the stage does"\ncmd = "python example_script.py --option"\ndeps = ["/path/to/input/file"]\nouts = ["/path/to/output/file"]\n```\n\nList the available stages with \n\n```\npython -m kewr list\n```\n\nRun each stage with \n\n```\npython -m kewr run stage1\n```\n\nYou can also run multiple stages at once with \n\n```\npython -m kewr run stage1 stage2 stage3\n```\n\nOr run all stages at once\n\n```\npython -m kewr run all\n```',
    'author': 'Henry Watkins',
    'author_email': 'h.watkins@ucl.ac.uk',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
