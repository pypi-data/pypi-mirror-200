from setuptools import setup, find_packages

version = '0.2'

setup(
    name='SmartTranslator',
    version=version,
    author='flw',
    author_email='flovvi78@gmail.com',
    packages=find_packages(exclude=['smart_translator.py']),
)