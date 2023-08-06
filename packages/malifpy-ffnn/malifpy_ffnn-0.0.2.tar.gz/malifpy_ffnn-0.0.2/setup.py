from setuptools import setup, find_packages
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='malifpy_ffnn',
    version='0.0.2',
    license='MIT',
    author="Muhammad Alif Putra Yasa",
    author_email='malifputrayasa@gmail.com',
    packages=find_packages('./'),
    package_dir={'': './'},
    url='https://github.com/malifpy/malifpy_ffnn',
    keywords='ffnn',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[
        'typing',
    ],
)
