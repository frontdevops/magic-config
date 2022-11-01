#!/usr/bin/env bash

#python setup.py sdist bdist_wheel
#twine upload --repository-url https://test.pypi.org/legacy/ dist/*
# check-manifest


echo "Delete current dist..."
rm -vrf dist
rm -vrf magic_config/magic_config.egg-info

python -m build

twine check dist/* && python -m twine upload --verbose dist/*


#python -m twine upload --verbose --repository testpypi dist/*
#python -m twine upload --verbose dist/*

