# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['testing', 'testing.fixtures', 'testing.package', 'testing.style']

package_data = \
{'': ['*']}

install_requires = \
['black>=23.1.0,<24.0.0',
 'isort>=5.12.0,<6.0.0',
 'mypy>=1.0.1,<2.0.0',
 'pytest-cov>=4.0.0,<5.0.0',
 'pytest>=7.2.2,<8.0.0',
 'ruff>=0.0.254,<0.0.255',
 'tomli>=2.0.1,<3.0.0']

setup_kwargs = {
    'name': 'geneweaver-testing',
    'version': '0.0.1a8',
    'description': 'A library to standardize testing of GeneWeaver pacakges.',
    'long_description': '# Geneweaver Testing\nThis package is used to test the Geneweaver project. It contains tools for running tests against Geneweaver project\npackages and components to aid in the development of Geneweaver. \n\n## Quick Start\n1. Install the package\n    ```bash\n    poetry install -G dev geneweaver-testing\n    ```\n2. Make a "common" test file\n    ```\n    touch tests/common.py\n    ```\n3. Add the following to the "common" test file\n    ```\n    # Inside tests/common.py\n    from geneweaver.testing import *\n    ```\n4. Add a fixture file at test root (if you don\'t have one already)\n    ```\n    touch tests/conftest.py\n    ```\n5. Add the following to the fixture file\n    ```\n    # Inside tests/conftest.py\n    from geneweaver.testing.fixtures import *\n    ```\n6. Run Tests!\n    ```bash\n    pytest tests\n    ```\n\n## Package Modules\nLike all Geneweaver packages, this package is namespaced under the `geneweaver` package. The root of this package is\n`geneweaver.testing`. The package is structured for usage in pytest tests, with pre-defined tests available through\nsplat (`*`) imports as shown in the Quick Start. Other package functionality is available by specifically importing\nmodules.\n\nThe following modules are available in this package:\n\n### `geneweaver.testing.fixtures`\nThis module contains pytest fixtures that are used to test Geneweaver packages. These fixtures can be used to set up\ntest contexts for Geneweaver packages. This module does not contain any tests.\n\n### `geneweaver.testing.package`\nThis module contains tools for testing and validating Geneweaver packages. \n\n\n## Contributing\nContributions to this package are welcome. Please see the [Contributing](CONTRIBUTING.md) document for more information.\n\n',
    'author': 'Alexander Berger',
    'author_email': 'alexander.berger@jax.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://bergsalex.github.io/geneweaver-docs/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
