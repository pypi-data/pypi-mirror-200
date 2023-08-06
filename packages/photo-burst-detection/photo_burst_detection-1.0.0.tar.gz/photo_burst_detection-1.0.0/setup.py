# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

setup(
    name='photo_burst_detection',
    version='1.0.0',
    author='batou9150',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
        'flask-login',
        'flask-ldap3-login',
    ],
    description='Flask App for photo burst detection',
    long_description=readme,
    long_description_content_type='text/markdown',
    url='https://gitlab.com/batou9150/photo_burst_detection',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
