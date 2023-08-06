from setuptools import setup, find_packages
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()
setup(
    name='libgpt',
    version='1.0.1',
    description='A module for using GPT-3/4 for free (Needs Chrome or Chromium browser for GPT-3)',
    author='csoftware',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[
        'selenium',
        'undetected-chromedriver'
    ]
)

