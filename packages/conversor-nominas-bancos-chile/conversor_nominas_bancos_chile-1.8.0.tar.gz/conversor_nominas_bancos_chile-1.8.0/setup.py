# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['conversor_nominas_bancos_chile']

package_data = \
{'': ['*'], 'conversor_nominas_bancos_chile': ['planillas_test/*']}

install_requires = \
['datetime>=5.1,<6.0',
 'numpy>=1.24.2,<2.0.0',
 'openpyxl>=3.1.2,<4.0.0',
 'pandas>=1.5.3,<2.0.0',
 'pathlib>=1.0.1,<2.0.0',
 'tk>=0.1.0,<0.2.0',
 'xlrd>=2.0.1,<3.0.0']

entry_points = \
{'console_scripts': ['start_menu_conversor_nominas = '
                     'conversor_nominas_bancos_chile.bank_tkinter_menu:iniciar_menu']}

setup_kwargs = {
    'name': 'conversor-nominas-bancos-chile',
    'version': '1.8.0',
    'description': 'Librería que convierte el formato de nóminas del BCI al formato del resto de bancos.',
    'long_description': None,
    'author': 'Antonio Canada Momblant',
    'author_email': 'toni.cm@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
