from setuptools import setup, find_packages

setup(
    name='data_utils',
    version='0.1.0',
    packages=find_packages(),
    description='Reusable utilities for data analysis',
    author='Jamil Mendez',
    install_requires=[
        'pandas'
        ,'os'
        ,'glob'
        ,'shutil'
        ,'pathlib'
    ],
)