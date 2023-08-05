from setuptools import setup, find_packages

setup(
    name='fmapping',
    version='0.1.0',
    author='Sleeping Cat',
    author_email='sleeping4cat@gmail.com',
    description='A library for extracting feature maps from images using Inception V3',
    packages=find_packages(),
    install_requires=[
        'tensorflow',
        'matplotlib',
        'numpy'
        
    ]
)
