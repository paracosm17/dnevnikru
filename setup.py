from setuptools import setup

setup(
    name='dnevnikru',
    version='1.0',
    packages=['dnevnikru'],
    url='https://github.com/paracosm17/dnevnikru',
    license='Apache License 2.0',
    author='paracosm17',
    author_email='paracosm17@yandex.ru',
    description='dnevnik.ru parser',
    install_requires=[
        'requests',
        'bs4',
        'lxml'
    ],
)
