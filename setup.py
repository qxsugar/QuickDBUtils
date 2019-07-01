# coding=utf-8
from setuptools import setup, find_packages

setup(
    name="QuickDBUtils",
    version='1.0',
    description='DBUtils的二次封装',
    py_modules=['QuickDBUtils'],
    author='qxsugar',
    author_email='qxsugar@gmail.com',
    install_requires=[
        "DBUtils>=1.3"
    ],
    packages = find_packages(),  
)
