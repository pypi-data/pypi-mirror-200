# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['mxcurpy']
setup_kwargs = {
    'name': 'mxcurpy',
    'version': '0.1.0',
    'description': 'Compute CURP and RFC for Mexican Citizens',
    'long_description': None,
    'author': 'Héctor Iván Patricio Moreno',
    'author_email': 'hectorivanpatriciomoreno@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
