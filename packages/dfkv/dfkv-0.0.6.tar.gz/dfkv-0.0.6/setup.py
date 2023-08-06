#!/usr/bin/env python
from io import open
from setuptools import setup, find_packages
# from distutils.core import setup
# setup(name="dfkv", version="0.0.6", description="test to install module", author="someone", py_modules=['dfkv.common'])
setup(
    name='dfkv',
    version='0.0.6',
    description='a expand for dict',
    long_description='expand dict, can use a.b, can set value more than 1-level a.b.c.d="xyz"',
    author='fred deng',
    author_email='dfgeoff@qq.com',
    license='Apache License 2.0',
    url='https://gitee.com/hifong45/dkv.git',
    download_url='https://gitee.com/hifong45/dkv/master.zip',
    packages=find_packages('src', exclude=["examples", "tests", "project"]), # can not be empty
    package_dir={'': 'src'}, # can not be empty
    install_requires=[]
)
# rd /s /q dist && python setup.py sdist && pip uninstall -y dfkv && pip install dist\dfkv-0.0.1.tar.gz
# 2023-01-28 16:16:52.993077