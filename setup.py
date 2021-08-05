from setuptools import setup

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='MongoDB Migration Tools',
    version='1.1.0',
    description='This tool allows you to copy a Mongo database from one cluster to another',
    long_description=readme,
    author='Flavio Augusto Rodrigues Tavares',
    license=license,
    packages=['src'],
    install_requires=['pytest', 'pytest-mock', 'jsondiff'],
    python_requires='>=3.5',
    zip_safe=False
)