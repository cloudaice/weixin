#-*-coding: utf-8-*-
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    "description": "weixin Public Accounts develop package",
    "author": "cloudaice(XiangChao)",
    "url": "url to get",
    "download_url": "url to download",
    "author_email": "cloudaice@gmail.com",
    "version": "0.1",
    "install_requires": [],
    "packages": ["weixin"],
    "scripts": [],
    "name": "weixin"
}

setup(**config)
