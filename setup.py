"""
Setup configuration for the Todo CLI application.
"""
from setuptools import setup, find_packages

setup(
    name="todo-cli",
    version="1.0.0",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'todo=src.cli.main:main',
        ],
    },
    install_requires=[],
    author="Todo CLI Team",
    description="A Python-based command-line Todo application with in-memory storage",
    python_requires='>=3.13',
)