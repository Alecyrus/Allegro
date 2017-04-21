"""
Sanic
"""
import codecs
import os
import re
from distutils.errors import DistutilsPlatformError
from distutils.util import strtobool

from setuptools import setup

with codecs.open(os.path.join(os.path.abspath(os.path.dirname(
        __file__)), 'enigma', '__init__.py'), 'r', 'latin1') as fp:
    try:
        version = re.findall(r"^__version__ = '([^']+)'\r?$",
                             fp.read(), re.M)[0]
    except IndexError:
        raise RuntimeError('Unable to determine version.')

setup_kwargs = {
    'name': 'Enifma',
    'version': version,
    'url': 'https://github.com/Alecyrus/Enigma',
    'license': 'MIT',
    'author': 'Alecyrus,
    'author_email': 'alecyrus@163.com',
    'description': (
        'A python backend integration framework'),
    'packages': ['enigma'],
    'platforms': 'any',
    'classifiers': [
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Web Environment',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5'
    ],
}

requirements = [
    pika,
    sanic,
]
try:
    setup_kwargs['install_requires'] = requirements
    setup(**setup_kwargs)
except DistutilsPlatformError as exception:
    setup_kwargs['install_requires'] = requirements
    setup(**setup_kwargs)
