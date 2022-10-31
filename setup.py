#!/usr/bin/env python3
import re
import sys
import pathlib
from setuptools import find_packages, setup

WORK_DIR = pathlib.Path(__file__).parent

# Check python version
MINIMAL_PY_VERSION = (3, 10, 8)
if sys.version_info < MINIMAL_PY_VERSION:
    raise RuntimeError('aiogram works only with Python {}+'.format('.'.join(map(str, MINIMAL_PY_VERSION))))


def get_description() -> str:
    """
    Read full description from 'README.rst'
    :return: description
    :rtype: str
    """
    with open('README.rst', 'r', encoding='utf-8') as f:
        return f.read()


def get_version() -> str:
    """
    Read version
    :return: str
    """
    txt = (WORK_DIR / 'pyproject.toml').read_text('utf-8')
    try:
        return re.findall(r"^version = \"([^']+)\"\r?$", txt, re.M)[0]
    except IndexError:
        raise RuntimeError('Unable to determine version.')


setup(
    name='magic_config',
    version=get_version(),
    license='MIT',
    author='Alexander Majorov',
    author_email='alexander.majorov@gmail.com',
    description=('Is a pretty simple library for working with configuration'
                 ' files based on the .env files and environment variables'
                 ),
    long_description=get_description(),
    long_description_content_type="text/markdown",
    url='https://github.com/frontdevops/magic-config',
    # download_url="https://github.com/mike-huls/toolbox_public/archive/refs/tags/0.0.3.tar.gz",
    project_urls={
        "Bug Tracker": "https://github.com/frontdevops/magic-config/issues",
    },
    keywords=["pypi", "config", "tutorial"],
    classifiers=[
        # 'Development Status :: 4 - Beta',
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10.8',
        'Programming Language :: Python :: 3.11',
        'Topic :: Software Development :: Libraries :: Application Utilities',
    ],
    package_dir={"": "magic_config"},
    packages=find_packages(where="magic_config", exclude=('tests', 'tests.*', 'examples.*', 'docs',)),
    include_package_data=False,
    python_requires='>=3.10.8',
    install_requires=[
        "python-dotenv>=0.21.0",
    ],
    extras_require={
        "dev": [
            "pytest >= 3.7",
            "check-manifest",
            "twine"
        ]
    },
)
