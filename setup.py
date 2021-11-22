from setuptools import setup
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='dnevnikru',
    version='1.3.2',
    packages=['dnevnikru'],
    url='https://github.com/paracosm17/dnevnikru',
    license='Apache License 2.0',
    author='paracosm17',
    author_email='paracosm17@yandex.ru',
    description='dnevnik.ru parser',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[
        'requests',
        'bs4',
        'lxml'
    ],
)
