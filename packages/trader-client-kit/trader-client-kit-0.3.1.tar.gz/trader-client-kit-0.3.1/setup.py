# !/usr/bin/env python
# -*- coding: utf-8 -*-

# __time__: 2021/10/20 __auth__: 
# __remark__: trader-cli setup

import os

from setuptools import setup, find_packages

ROOT_PATH = os.path.abspath(os.path.dirname(__file__))
def get_file(base, path): return os.path.join(ROOT_PATH, base, path)

config = {}

config['name'] = 'trader-client-kit'
config['version'] = 'v0.3.1'
config['description'] = 'Trader - a common tool for blockchain'
config['keywords'] = 'trader-cli'
config['author'] = 'remy'
config['author_email'] = 'remy.ace@outlook.com'
config['license'] = 'MIT License'
config['packages'] = find_packages()
config['include_package_data'] = True
config['zip_safe'] = True

# config['data_files'] =[
#     ('trader/_source', ['config/logging.conf', 'config/trader.conf']),
# #     # (get_file('trader', '_source/'), ['conf/logging.conf', 'conf/trader.conf'])
# ]

config['classifiers'] = [
    'Programming Language :: Python :: 3',
    'Operating System :: OS Independent',
    'Development Status :: 1 - Planning',
    'Topic :: Utilities'
]

config['entry_points'] = {
    'console_scripts': ['trader=trader.__main__:main']
}

config['install_requires'] = [
    'web3==5.30.0',
    'python-dotenv==1.0.0',
    'python-okx==0.1.6'
]

setup(**config)