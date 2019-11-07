#!/usr/bin/env python3

import setuptools

import archive_to_s3


setuptools.setup(
    name='archive-to-s3',
    version=archive_to_s3.__version__,
    packages=setuptools.find_packages(),
    install_requires=[
        'pytoolbox[aws]>=13.0.4<14',
        'JSON-log-formatter>=0.2.0<1.0'
    ],
    entry_points={
        'console_scripts': [
            'archive-to-s3=archive_to_s3.process:main'
        ]
    },

    # Meta-data for upload to PyPI
    author='David Fischer',
    author_email='david@fisch3r.net',
    classifiers=[
        # https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: European Union Public Licence 1.1 (EUPL 1.1)',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: System :: Archiving',
        'Topic :: System :: Archiving :: Backup',
        'Topic :: System :: Archiving :: Mirroring'
    ],
    description='',
    keywords=['archive', 'aws', 's3'],
    license='EUPL 1.1',
    long_description=open('README.rst', 'r', encoding='utf-8').read(),
    url='https://github.com/davidfischer-ch/archive-to-s3'
)
