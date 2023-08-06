# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['optiframe', 'optiframe.framework', 'optiframe.workflow_engine']

package_data = \
{'': ['*']}

install_requires = \
['pulp>=2.7.0,<3.0.0']

entry_points = \
{'console_scripts': ['knapsack = examples.knapsack:demo']}

setup_kwargs = {
    'name': 'optiframe',
    'version': '0.1.0',
    'description': 'A modular framework for mixed integer programming',
    'long_description': '# Optiframe\n\nOptiframe is an **opti**mization **frame**work for writing mixed integer programs (MIPs).\n\nIt allows you to structure your MIPs in a way that allows clear separation of concerns,\nhigh modularity and testability.\n\n## Core Concepts\n\n- The optimization process is divided into multiple **steps** which are clearly separated:\n  1. **Validation** allows you to validate the input data.\n  2. **MIP building** allows you to modify the MIP to define the optimization problem.\n  3. **Solving** is a pre-defined step that obtains an optimal solution for the problem.\n  4. **Solution extraction** allows you to process the variable values of the solution into something more meaningful.\n- **Tasks** are the core components that allow you to implement functionality for each step.\n  - The constructor of a task allows you to define *dependencies* for that task,\n    which are automatically injected by the optimizer based on their type annotation.\n  - The **execute** method allows you to implement the functionality.\n    It may return data which can then be used by other tasks as a dependency.\n- **Packages** combine tasks that belong together.\n    Each package must contain a task for building the MIP and can additionally contain tasks\n    for validation and solution extraction.\n    The packages are what makes Optiframe so modular:\n    You can define extensions of a problem in a separate package and only include it if needed.\n- The **optimizer** allows you to configure the packages that you need.\n    Afterwards, you can initialize it with the instance data and then solve the optimization problem.\n\n## Installation & Usage\n\n```cli\npip install optiframe\n```\n\nTake a look at the `examples` folder for examples on how to use Optiframe!\n\n## License\n\nThis project is available under the terms of the [MIT license](LICENSE).\n',
    'author': 'Tim Jentzsch',
    'author_email': 'optiframe.projects@timjen.net',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/TimJentzsch/optiframe',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.11.0rc1',
}


setup(**setup_kwargs)
