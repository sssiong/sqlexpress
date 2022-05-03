from pathlib import Path
from setuptools import setup, find_packages

PROJECT_DIR = Path(__file__).parent

long_description = (PROJECT_DIR / 'README.md').read_text()

setup(
    name='sqlexpress',
    version='0.1.0',
    author='sssiong',
    description='Package to parse SQL scripts for information',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/sssiong/sqlexpress',
    install_requires=[
        'networkx==2.8',
        'PyYAML==6.0',
    ],
    tests_require=['pytest'],
    packages=find_packages(exclude=('tests', )),
)