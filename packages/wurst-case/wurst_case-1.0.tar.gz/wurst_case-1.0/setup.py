from setuptools import setup
# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()


setup(name='wurst_case', version='1.0',
description='Hi this is my first random package',
long_description = 'spp package hello world', author='healpa',
packages=['wurst_case', 'wurst_case.subpack'],
)
