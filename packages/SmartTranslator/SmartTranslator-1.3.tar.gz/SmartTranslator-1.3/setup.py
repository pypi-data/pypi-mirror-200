from setuptools import setup, find_packages

version = '1.3'
requirements = ["setuptools~=58.1.0", "googletrans~=4.0.0rc1", "pyaspeller~=0.2.3"]

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

setup(
    name='SmartTranslator',
    version=version,
    author='flw',
    author_email='flovvi78@gmail.com',
    packages=find_packages(exclude=['smart_translator.py']),
    install_requires=requirements,
    long_description=readme,
    long_description_content_type="text/markdown",
)

# python setup.py sdist
# twine upload dist/*