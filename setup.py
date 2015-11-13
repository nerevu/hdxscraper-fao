import sys
from os import path as p
from config import _project

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages


def read(filename, parent=None):
    parent = (parent or __file__)

    try:
        with open(p.join(p.dirname(parent), filename)) as f:
            return f.read()
    except IOError:
        return ''


def parse_requirements(filename, parent=None):
    parent = (parent or __file__)
    filepath = p.join(p.dirname(parent), filename)
    content = read(filename, parent)

    for line_number, line in enumerate(content.splitlines(), 1):
        candidate = line.strip()

        if candidate.startswith('-r'):
            for item in parse_requirements(candidate[2:].strip(), filepath):
                yield item
        else:
            yield candidate

# Avoid byte-compiling the shipped template
sys.dont_write_bytecode = True
gh = 'https://github.com/reubano'

config = {
    'description': 'Collector for UN Food and Agriculture Organization (FAO) Humanitarian Data',
    'name': _project,
    'long_description': open('README.md', 'rt').read(),
    'author': 'Reuben Cummings',
    'url': '%s/%s' % (gh, _project),
    'download_url': '%s/%s/downloads/%s*.tgz' % (gh, _project, _project),
    'author_email': 'reubano@gmail.com',
    'version': '0.6.0',
    'install_requires': parse_requirements('requirements.txt'),
    'classifiers': [
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: The MIT License (MIT)',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: Microsoft :: POSIX'
    ],
    'keywords': 'api',
    'type': 'api',
    'packages': find_packages(exclude=['tests']),
    'package_data': {},
    'include_package_data': True,
    'zip_safe': False,
    'license': 'MIT',
    'platforms': ['MacOS X', 'Windows', 'Linux'],
    'include_package_data': True
}

setup(**config)
