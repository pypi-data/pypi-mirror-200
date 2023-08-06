# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mass_composition', 'mass_composition.utils']

package_data = \
{'': ['*'], 'mass_composition': ['config/*']}

install_requires = \
['periodictable>=1.6.1,<2.0.0',
 'pyyaml>=6.0,<7.0',
 'scipy>=1.9.0,<2.0.0',
 'xarray>=2022.6.0,<2023.0.0']

extras_require = \
{'network': ['networkx>=3.0,<4.0'],
 'viz': ['pyvista>=0.37.0,<0.38.0',
         'pyvista-xarray>=0.1.2,<0.2.0',
         'matplotlib>=3.6.2,<4.0.0',
         'plotly>=5.13.0,<6.0.0',
         'kaleido==0.2.1',
         'seaborn>=0.12.2,<0.13.0']}

setup_kwargs = {
    'name': 'mass-composition',
    'version': '0.1.8',
    'description': 'For managing multi-dimensional mass-composition datasets, supporting weighted mathematical operations and visualisation.',
    'long_description': 'None',
    'author': 'Greg',
    'author_email': 'greg@elphick.com.au',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4',
}


setup(**setup_kwargs)
