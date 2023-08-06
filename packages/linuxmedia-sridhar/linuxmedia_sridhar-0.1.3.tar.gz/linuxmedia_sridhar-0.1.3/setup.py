from setuptools import setup, find_packages
import os


requirements = os.popen("/usr/local/bin/pipreqs main --print").read().splitlines()
with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()


setup(
    name='linuxmedia_sridhar',
    version='0.1.3',
    author='Sridhar',
    author_email='dcsvsridhar@gmail.com',
    description='Linuxmedia is a wrapper for 60 above 60+ Linux Commands',
    packages=find_packages(),
    url='https://git.selfmade.ninja/SRIDHARDSCV/packaging_own_cli_tool',
    install_requires=requirements,
    # install_requires=[],
    long_description=long_description,
    long_description_content_type='text/markdown',
    entry_points={
        'console_scripts': [
            'linuxmedia=main.main:main',
        ],
    },
)