import os

import setuptools

envstring = lambda var: os.environ.get(var) or ""

VERSION = [1, 2, 38]


try:
    with open("README.md", "r") as fh:
        long_description = fh.read()
except:
    long_description = ""

setuptools.setup(
    name="e6xdb",
    version='.'.join('%d' % v for v in VERSION[0:3]),
    author="Uniphi, Inc.",
    author_email="info@e6data.io",
    url=envstring("URL"),
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=[
        'sqlalchemy>=1.0.0',
        'future',
        'python-dateutil',
        'pycryptodome',
        'pytz',
        'thrift',
    ],
    classifiers=[
        "Operating System :: POSIX :: Linux",
        "License :: OSI Approved :: MIT License",
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9'
    ],
    entry_points={
        'sqlalchemy.dialects': [
            'e6xdb = e6xdb.sqlalchemy_e6x:E6xDialect'
        ],
    }
)
