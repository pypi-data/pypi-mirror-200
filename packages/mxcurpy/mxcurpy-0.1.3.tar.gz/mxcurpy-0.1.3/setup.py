# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mxcurpy']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'mxcurpy',
    'version': '0.1.3',
    'description': 'Compute CURP and RFC for Mexican Citizens',
    'long_description': '# MXCurpy\n\nGeneración de Clave Única de Registro de Población y el Registro Federal de Contibuyentes de México en Python.\n\nDocumentos en los que está basado este paquete:\n\nCURP: (/docs/dof18102021.pdf)[INSTRUCTIVO NORMATIVO PARA LA ASIGNACIÓN DE LA CLAVE ÚNICA DE REGISTRO DE\nPOBLACIÓN]\n\nRFC:\n\n## Estado actual del proyecto\n\nPor el momento está funcionando la creación de CURP, por lo que he decidido liberarlo para poder usarlo.\n\n## Uso\n\n```python\nfrom mxcurpy.curp import curp\n\nmy_curp = curp(names="Juan José", lastname="Martínez", second_lastname="Pérez", birth_date="12-08-1989", birth_state="Durango", sex="h")\n\n# MAPJ890812HDGRRN00\n\n```\n\n## Consideraciones\n\n\n## Lista de estados válidos\n\nEstados:\n\n* "AGUASCALIENTES"\n* "BAJA CALIFORNIA"\n* "BAJA CALIFORNIA SUR"\n* "CAMPECHE"\n* "COAHUILA"\n* "COLIMA"\n* "CHIAPAS"\n* "CHIHUAHUA"\n* "DISTRITO FEDERAL"\n* "CDMX"\n* "CIUDAD DE MEXICO"\n* "DURANGO"\n* "GUANAJUATO"\n* "GUERRERO"\n* "HIDALGO"\n* "JALISCO"\n* "MEXICO"\n* "MICHOACAN"\n* "MORELOS"\n* "NAYARIT"\n* "NUEVO LEON"\n* "OAXACA"\n* "PUEBLA"\n* "QUERETARO"\n* "QUINTANA ROO"\n* "SAN LUIS POTOSI"\n* "SINALOA"\n* "SONORA"\n* "TABASCO"\n* "TAMAULIPAS"\n* "TLAXCALA"\n* "VERACRUZ"\n* "YUCATAN"\n* "ZACATECAS"\n* "NACIDO EN EL EXTRANJERO"\n\n## LICENCIA\n\nMIT\n',
    'author': 'Héctor Iván Patricio Moreno',
    'author_email': 'hectorivanpatriciomoreno@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/hectorip/mxcurpy',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
