# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['osmrx',
 'osmrx.apis_handler',
 'osmrx.data_processing',
 'osmrx.globals',
 'osmrx.helpers',
 'osmrx.topology']

package_data = \
{'': ['*']}

install_requires = \
['more-itertools>=9.1.0,<10.0.0',
 'requests-futures>=1.0.0,<2.0.0',
 'rtree>=1.0.1,<2.0.0',
 'scipy>=1.10.1,<2.0.0',
 'shapely>=2.0.1,<3.0.0']

setup_kwargs = {
    'name': 'osmrx',
    'version': '0.0.3',
    'description': '',
    'long_description': '# osmNetwork\n\n![CI](https://github.com/amauryval/osmNetwork/workflows/RunTest/badge.svg)\n\n[![codecov](https://codecov.io/gh/amauryval/osmNetwork/branch/master/graph/badge.svg)](https://codecov.io/gh/amauryval/osmNetwork)\n\n\n## Dev Env install\n\n```bash\npyenv local 3.11.0\npoetry env use 3.11.0\npoetry install\n```\n',
    'author': 'amauryval',
    'author_email': 'amauryval@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '==3.11.0',
}


setup(**setup_kwargs)
