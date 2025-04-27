# setup.py
from setuptools import setup, find_packages

setup(
    name='file_manager',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'file-manager-cli = file_manager.cli:main'
        ]
    },
)
