#!/usr/bin/env python3
import pathlib
import re
import sys

from setuptools import find_packages, setup

WORK_DIR = pathlib.Path(__file__).parent

# Check python version
MINIMAL_PY_VERSION = (3, 10)
if sys.version_info < MINIMAL_PY_VERSION:
    raise RuntimeError('aiogram works only with Python {}+'.format('.'.join(map(str, MINIMAL_PY_VERSION))))


def get_description() -> str:
    """
    Read full description from 'README.rst'
    :return: description
    :rtype: str
    """
    with open('../README.rst', 'r', encoding='utf-8') as f:
        return f.read()


def get_version() -> str:
    """
    Read version
    :return: str
    """
    txt = (WORK_DIR / 'src' / 'magic_config' / '__init__.py').read_text('utf-8')
    try:
        return re.findall(r"^__version__ = '([^']+)'\r?$", txt, re.M)[0]
    except IndexError:
        raise RuntimeError('Unable to determine version.')


setup(
    name='magic_config_geekjob',
    version=get_version(),
    packages=find_packages(exclude=('tests', 'tests.*', 'examples.*', 'docs',)),
    url='https://github.com/frontdevops/magic-config',
    license='MIT',
    author='Alexander Majorov',
    python_requires='>=3.10.8',
    author_email='alexander.majorov@gmail.com',
    description=('Is a pretty simple library for working with configuration'
                 ' files based on the .env files and environment variables'
                 ),
    long_description=get_description(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Framework :: None',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.10.8',
        'Programming Language :: Python :: 3.11',
        'Topic :: Software Development :: Libraries :: Application Utilities',
    ],
    install_requires=[
        'python-dotenv>=0.21.0',
    ],
    include_package_data=False,
)
