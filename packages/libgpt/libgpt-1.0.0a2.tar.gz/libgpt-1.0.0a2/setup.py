from setuptools import setup, find_packages
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()
setup(
    name='libgpt',
    version='1.0.0 Alpha 2',
    description='A module for using the ChatGPT Free (Needs Chrome or Chromium browser)',
    author='csoftware',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[
        'selenium',
        'undetected-chromedriver'
    ]
)

