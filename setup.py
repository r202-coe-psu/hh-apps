'''
HH-service
----------

A service core for HomeHero
'''

import re
import ast
from setuptools import setup


_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('hhapps/__init__.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
            f.read().decode('utf-8')).group(1)))
setup(
    name='hhapps',
    version=version,
    url='',
    license='',
    author='',
    author_email='',
    description='A application service for HomeHero',
    long_description=__doc__,
    packages=['hhapps'],
    include_package_data=True,
    install_requires=[
        'flask',
        'marshmallow-jsonapi',
        'marshmallow-jsonschema',
        'mongoengine',
        'flask-mongoengine',
        'flask-jwt-extended'
    ],
    dependency_links=[
        'https://github.com/fuhrysteve/marshmallow-jsonschema/tarball/master#egg'
    ],
    classifiers=[
    ],
    entry_points='''
        [console_scripts]
        hhapps-inventory-api=hhapps.cmd.inventory_api:main
        hhapps-nutrition-api=hhapps.cmd.nutrition_api:main
    '''
)
