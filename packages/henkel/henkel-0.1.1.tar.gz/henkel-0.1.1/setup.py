from setuptools import setup, find_packages

setup(
    name='henkel',
    version='0.1.1',
    description='Pytorch Library for Henkel',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
        'sklearn',
        'torch'
        ],
    author='Deep Raj',
    author_email='deeprajshrivastava132@gmail.com',
    url='https://github.com/yourusername/mylibrary'
)
