# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['bloghead', 'bloghead.persistence']

package_data = \
{'': ['*'], 'bloghead': ['icons/*']}

install_requires = \
['peewee>=3.16.0,<4.0.0', 'pyside2>=5.15.2.1,<6.0.0.0']

entry_points = \
{'console_scripts': ['bloghead = bloghead:start']}

setup_kwargs = {
    'name': 'bloghead',
    'version': '0.1.0',
    'description': '',
    'long_description': '# WIP\n\nThe plan is to rewrite [bloghead](https://github.com/nhanb/bloghead) but this\ntime as a proper Qt application. Nothing but the mockup UI has been done yet.\n\n![](mockup.png)\n\n# Dependencies\n\nAssumes nodejs (command `node`) is available in $PATH.\n',
    'author': 'Nhân',
    'author_email': 'hi@imnhan.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<3.11',
}


setup(**setup_kwargs)
