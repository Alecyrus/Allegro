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
        __file__)), 'allegro', '__init__.py'), 'r', 'latin1') as fp:
    try:
        version = re.findall(r"^__version__ = '([^']+)'\r?$",
                             fp.read(), re.M)[0]
    except IndexError:
        raise RuntimeError('Unable to determine version.')

setup_kwargs = {
    'name': 'Allegro',
    'version': version,
    'url': 'https://github.com/Alecyrus/Allegro',
    'license': 'MIT',
    'author': 'Alecyrus',
    'author_email': 'alecyrus@163.com',
    'description': (
        'A python backend integration framework'),
    'packages': ['allegro'],
    'platforms': 'any',
    'classifiers': [
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Web Environment',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5'
    ],
}

requirements = [
    'aiofiles==0.3.1',
    'amqp==2.1.4',
    'appdirs==1.4.3',
    'billiard==3.5.0.2',
    'celery==4.0.2',
    'enum-compat==0.0.2',
    'eventlet==0.21.0',
    'greenlet==0.4.12',
    'httptools==0.0.9',
    'kombu==4.0.2',
    'packaging==16.8',
    'pyparsing==2.2.0',
    'pytz==2017.2',
    'redis==2.10.5',
    'sanic==0.5.4',
    'six==1.10.0',
    'ujson==1.35',
    'uvloop==0.8.0',
    'vine==1.1.3',
    'websockets==3.3'
]
try:
    setup_kwargs['install_requires'] = requirements
    setup(**setup_kwargs)
except DistutilsPlatformError as exception:
    setup_kwargs['install_requires'] = requirements
    setup(**setup_kwargs)
