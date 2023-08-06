from setuptools import setup

with open("./README.txt", "r") as f:
    long_description = f.read()

setup(
    name='custom-vsearch',
    version='1.0',
    description='Search for specific letters into a given phrase.',
    author='Ariel Denaro',
    url='',
    py_modules=['vsearch'], #This is a list of .py files to include, here we have only one.
    long_description=long_description
)