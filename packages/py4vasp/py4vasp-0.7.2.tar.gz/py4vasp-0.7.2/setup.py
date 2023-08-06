# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['py4vasp',
 'py4vasp._control',
 'py4vasp._data',
 'py4vasp._raw',
 'py4vasp._third_party',
 'py4vasp._third_party.graph',
 'py4vasp._util',
 'py4vasp.scripts']

package_data = \
{'': ['*']}

install_requires = \
['ase>=3.22.1',
 'h5py>=3.7.0',
 'ipywidgets>=7.7,<8.0',
 'kaleido!=0.2.1.post1,>=0.2.1',
 'mdtraj>=1.9.6',
 'mrcfile>=1.3.0',
 'nglview>=3.0.3',
 'numpy>=1.23.0',
 'pandas>=1.4.3',
 'plotly>=5.9.0']

entry_points = \
{'console_scripts': ['error-analysis = py4vasp.scripts.error_analysis:main']}

setup_kwargs = {
    'name': 'py4vasp',
    'version': '0.7.2',
    'description': 'Tool for assisting with the analysis and setup of VASP calculations.',
    'long_description': '# py4vasp\n\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![tests](https://github.com/vasp-dev/py4vasp/actions/workflows/test.yml/badge.svg)](https://github.com/vasp-dev/py4vasp/actions/workflows/test.yml)\n\n> Please note that this document is intended mostly for developers that want to use\n> the version of py4vasp provided on Github. If you just want to install py4vasp to\n> use it, please follow the [official documentation](https://vasp.at/py4vasp/latest).\n\n## Installation\n\nWe use the [poetry dependency manager](https://python-poetry.org/) which takes care of\nall dependencies and maintains a virtual environment to check the code. If you want to\ntest something in the virtual environment, just use e.g. ```poetry run jupyter-notebook```.\n\nUsing poetry installing and the code requires the following steps. The last step will\ntest whether everything worked\n~~~shell\ngit clone git@github.com:vasp-dev/py4vasp.git\npip install poetry\npoetry install\npoetry run pytest\n~~~\nNote that this will install py4vasp into a virtual environment managed by poetry. This\nisolates the code from all other packages you have installed and makes sure that when\nyou modify the code all the relevant dependencies are tracked.\n\nOccasionally, we encountered errors when installing the *mdtraj* dependency in this\nfashion, in particular on MacOS and Windows. If you notice the same behavior, we\nrecommend to manage your environment with *conda* and install *py4vasp* in the\nfollowing manner\n~~~shell\ngit clone git@github.com:vasp-dev/py4vasp.git\nconda create --name py4vasp-env python=3.8\nconda activate py4vasp-env\nconda install -c conda-forge poetry\nconda install -c conda-forge mdtraj\npoetry config virtualenvs.create false --local\npoetry install\npoetry run pytest\n~~~\n\n## Code style\n\nCode style is enforced, but is not something the developer should spend time on, so we\ndecided on using the black formatter. Please run ```black .``` before committing the code.\n\n## Contributing to py4vasp\n\nWe welcome contributions to py4vasp. To improve the code please follow this workflow\n\n* Create an issue for the bugfix or feature you plan to work on, this gives the option\n  to provide some input before work is invested.\n* Implement your work in a fork of the repository and create a pull request for it.\n  Please make sure to test your code thoroughly and commit the tests in the pull\n  request in the tests directory.\n* In the message to your merge request mention the issue the code attempts to solve.\n* We will try to include your merge request rapidly when all the tests pass and your\n  code is covered by tests.\n\nPlease limit the size of a pull request to approximately 200 lines of code\notherwise reviewing the changes gets unwieldy. Prefer splitting the work into\nmultiple smaller chunks if necessary.\n',
    'author': 'VASP Software GmbH',
    'author_email': 'py4vasp@vasp.at',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://vasp.at/py4vasp/latest',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4',
}


setup(**setup_kwargs)
