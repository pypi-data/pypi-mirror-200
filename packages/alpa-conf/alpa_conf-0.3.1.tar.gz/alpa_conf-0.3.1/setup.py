# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['alpa_conf']

package_data = \
{'': ['*']}

install_requires = \
['pyyaml>=5.0']

setup_kwargs = {
    'name': 'alpa-conf',
    'version': '0.3.1',
    'description': 'Wrapper around configuration files for packit and alpa',
    'long_description': '### alpa-conf\n\nWrapper around configuration files for packit and alpa\n',
    'author': 'Jiri Kyjovsky',
    'author_email': 'j1.kyjovsky@gmail.com',
    'maintainer': 'Jiří Kyjovský',
    'maintainer_email': 'j1.kyjovsky@gmail.com',
    'url': 'https://github.com/alpa-team/alpa-conf',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
