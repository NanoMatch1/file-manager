# setup.py

from setuptools import setup, find_packages

setup(
    name='file_manager',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'typer[all]',  # <-- add typer as dependency
    ],
    entry_points={
        'console_scripts': [
            'file-manager-cli = file_manager.cli:app',  # <--- changed from main() to app
        ]
    },
)
