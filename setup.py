from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='pueda',
    version='0.1.0',
    license='Apache 2.0',
    author="Marco Merlin",
    author_email='marcomerli@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    description="Collection of python for micro-Electronic Design Automation",
    url='https://github.com/bat52/pueda',
    keywords='python EDA CAD',
    package_data = {
    'icarus/src': ['*.v']
    'icarus/inc': ['*.vh']
    }
    install_requires=[
          # 'shutil',
          'wget',
          'edalize',
          'pyverilator',
          'dtrx',
          'myhdl',
          'veriloggen',
          ],
)
