"""Setup script for stock.

This script will install stock as a Python module.

"""

import pathlib
from setuptools import find_packages
from setuptools import setup

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / 'README.md').read_text(encoding='utf-8')

stock_description = "stock: Taiwan stock crawler and analysis tool."

install_requires = ["requests >= 2.24.0", "pymongo >= 3.11.0", "lxml >= 4.6.1 "]

setup(
    name="stock",
    version="0.1.0",
    description=stock_description,
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/Jyun-Neng/stock",
    authur="Jyun-Neng Ji",
    packages=find_packages(),
    install_requires=install_requires)
