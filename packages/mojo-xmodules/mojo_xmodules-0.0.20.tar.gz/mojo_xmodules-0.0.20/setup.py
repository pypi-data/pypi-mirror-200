# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'source/packages'}

packages = \
['mojo',
 'mojo.factories',
 'mojo.protocols.power.dlipower',
 'mojo.protocols.serial',
 'mojo.protocols.ssh',
 'mojo.xmods',
 'mojo.xmods.credentials',
 'mojo.xmods.eventing',
 'mojo.xmods.extension',
 'mojo.xmods.interfaces',
 'mojo.xmods.landscaping',
 'mojo.xmods.landscaping.agents',
 'mojo.xmods.landscaping.coordinators',
 'mojo.xmods.landscaping.coupling',
 'mojo.xmods.landscaping.layers',
 'mojo.xmods.wellknown',
 'mojo.xmods.xcollections',
 'mojo.xmods.xlogging',
 'mojo.xmods.xthreading']

package_data = \
{'': ['*']}

install_requires = \
['debugpy>=1.6.6,<2.0.0',
 'mojo-waiting>=1.0.0,<2.0.0',
 'paramiko>=3.1.0,<4.0.0']

setup_kwargs = {
    'name': 'mojo-xmodules',
    'version': '0.0.20',
    'description': 'Automation Mojo X-Modules',
    'long_description': '# Automation Mojo X-Modules (mojo-xmodules)\nThis package contains helper modules that extend the function of standard python modules.\n\n',
    'author': 'None',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
