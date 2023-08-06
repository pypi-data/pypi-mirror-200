__author__="Ayush Yajnik"

import setuptools
from setuptools import setup, find_packages
from typing import List

setuptools.setup(
    include_package_data=True,
    name="CyberArk_KeyVault",
    version= '0.0.1',
    description="CyberArk python helper function",
    long_description_content_type="text/markdown",
    author="Ayush Yajnik",
    author_email="ayushyajnik1@outlook.com",
    packages = find_packages(),
    install_requires = [
    "alembic==1.9.2",
    "bpy==3.4.0",
    "certifi==2022.12.7",
    "charset-normalizer==3.1.0",
    "click==8.1.3",
    "colorama==0.4.6",
    "Cython==0.29.33",
    "distlib==0.3.4",
    "filelock==3.7.0",
    "Flask==2.2.2",
    "Flask-Login==0.6.2",
    "Flask-Migrate==4.0.2",
    "Flask-SQLAlchemy==3.0.2",
    "Flask-WTF==1.1.1",
    "greenlet==2.0.1",
    "idna==3.4",
    "itsdangerous==2.1.2",
    "Jinja2==3.1.2",
    "Mako==1.2.4",
    "MarkupSafe==2.1.2",
    "numpy==1.24.2",
    "platformdirs==2.5.2",
    "python-dotenv==0.21.1",
    "requests==2.28.2",
    "pandas==1.5.3"
    ]
    )
