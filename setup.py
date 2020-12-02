"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""
import os
import sys

from setuptools import setup, find_packages

# pylint: disable=redefined-builtin

here = os.path.abspath(os.path.dirname(__file__))  # pylint: disable=invalid-name

with open(os.path.join(here, 'README.rst'), encoding='utf-8') as fid:
    long_description = fid.read()  # pylint: disable=invalid-name

with open(os.path.join(here, 'requirements.txt'), encoding='utf-8') as fid:
    install_requires = [
        line for line in fid.read().splitlines() if line.strip()
    ]

setup(
    name='bimrai',
    # Don't forget to update the version in __init__.py and CHANGELOG.rst!
    version='0.0.0',
    description='Visualize BIMRAI scenarios.',
    long_description=long_description,
    url='https://github.com/mristin/bimrai',
    author='Marko Ristin',
    author_email='marko.ristin@gmail.com',
    classifiers=[
        # yapf: disable
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8'
        # yapf: enable
    ],
    license='License :: OSI Approved :: MIT License',
    keywords='BIM architecture civil engineering requirements',
    packages=find_packages(exclude=['tests']),
    install_requires=install_requires,
    extras_require={
        'dev': [
            # yapf: disable
            # yapf: enable
        ],
    },
    py_modules=['bimrai'],
    package_data={"bimrai": ["py.typed"]},
    data_files=[('.', ['LICENSE', 'README.rst', 'requirements.txt'])]
)
