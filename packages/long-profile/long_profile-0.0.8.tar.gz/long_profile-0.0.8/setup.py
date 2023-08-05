# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src\\main\\python'}

packages = \
['pyLong',
 'pyLong.annotations',
 'pyLong.dictionnaries',
 'pyLong.groups',
 'pyLong.layouts',
 'pyLong.lists',
 'pyLong.misc',
 'pyLong.profiles',
 'pyLong.project',
 'pyLong.toolbox',
 'pyLong.toolbox.evofond']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.6.2,<4.0.0',
 'numpy>=1.24.1,<2.0.0',
 'pandas>=1.5.2,<2.0.0',
 'pyshp>=2.3.1,<3.0.0',
 'rdp>=0.8,<0.9',
 'scipy>=1.9.3,<2.0.0',
 'simpledbf>=0.2.6,<0.3.0',
 'visvalingamwyatt>=0.2.0,<0.3.0']

setup_kwargs = {
    'name': 'long-profile',
    'version': '0.0.8',
    'description': '',
    'long_description': 'None',
    'author': 'ONF-RTM',
    'author_email': 'None',
    'maintainer': 'Clément Roussel',
    'maintainer_email': 'clement.roussel@onf.fr',
    'url': 'https://www.onf.fr/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
