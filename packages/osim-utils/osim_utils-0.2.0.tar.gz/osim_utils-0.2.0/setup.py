# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['osim_utils', 'osim_utils.clients']

package_data = \
{'': ['*']}

install_requires = \
['python-json-logger>=2.0.4,<3.0.0', 'requests>=2.28.2,<3.0.0']

setup_kwargs = {
    'name': 'osim-utils',
    'version': '0.2.0',
    'description': '',
    'long_description': '# osim-utils\n\nThis package contains resources that are useful to more than one OSIM project. It includes, for\nexample, API clients to common literature resources, such as Europe PMC.\n\n## Installation\n\n```\npip install osim-utils\n```\n',
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
