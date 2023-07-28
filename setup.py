from setuptools import setup, find_packages
import os

datadir = os.path.join('data','icarus')
datafiles = [(d, [os.path.join(d,f) for f in files])
    for d, folders, files in os.walk(datadir)]

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='pueda',
    version='0.1.7',
    license='Apache 2.0',
    author="Marco Merlin",
    author_email='marcomerli@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    description="Collection of python for micro-Electronic Design Automation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/bat52/pueda',
    keywords='python EDA CAD',
    data_files = datafiles, 
    install_requires=[
          'wget',
          'edalize',
          'pyverilator-mm',
          'dtrx',
          'myhdl',
          'veriloggen',
          'pyvcd',
          'vcdvcd',
          'numpy'
          ],
)
