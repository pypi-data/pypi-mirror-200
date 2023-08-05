from setuptools import setup, find_packages

setup(
    name='my_python_package007',
    version='0.4.7',
    description='My awesome Python package v2',
    author='DipakMehta',
    author_email='dipak@zvolv.com',
    url='https://github.com/DipakMehta/python',
    long_description='we are trying new version',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',# list of dependencies
    ],
)
