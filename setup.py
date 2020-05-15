from setuptools import setup, find_packages

setup(
    name='crownstone-lib-python-cloud',
    version='1.0',
    url='https://github.com/RicArch97/crownstone-lib-python-cloud',
    author='Ricardo Steijn',
    description='Async library to get & store data from the Crownstone cloud.',
    packages=find_packages(exclude=['examples']),
    platforms='any',
    install_requires=list(package.strip() for package in open('requirements.txt')),
    classifiers=[
        'Programming Language :: Python :: 3.7'
    ]
)