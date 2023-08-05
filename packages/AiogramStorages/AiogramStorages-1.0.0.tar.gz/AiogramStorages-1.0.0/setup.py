from io import open
from setuptools import setup

version = '1.0.0'

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()


setup(
    name="AiogramStorages",
    version=version,
    author="DIMFLIX",
    author_email="dimflix.official@gmail.ru",
    description=(
        u'Save your data and states in aiogram bot.'
        u'Aiogram-storages was created to extend the standard fsm_storage options in aiogram.'
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DIMFLIX-OFFICIAL/AiogramStorages",
    download_url="https://github.com/DIMFLIX-OFFICIAL/AiogramStorages/archive/refs/heads/main.zip",
    license="MIT License",
    packages=['AiogramStorages'],
    install_requires=['aiogram', 'jsonpickle', 'asyncpg', 'aiosqlite'],
    classifiers=[
        "Operating System :: OS Independent",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Programming Language :: Python :: Implementation :: CPython"
    ]


)
