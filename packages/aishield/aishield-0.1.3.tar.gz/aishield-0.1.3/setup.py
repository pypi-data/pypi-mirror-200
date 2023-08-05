from setuptools import setup, find_packages

# To use a consistent encoding
from codecs import open
from os import path

# packages = \
# ['image_classification',
#  'utils']

# The directory containing this file
HERE = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# This call to setup() does all the work
setup(
    name="aishield",
    version="0.1.3",
    description="AIShield provides the Python convenience package to allow users to seamlessly integrate AIShield Vulnerability Assessment and Defense capabilities into their AI development workflows.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://www.boschaishield.com/',
    author="Contact AIShield",
    author_email="aishield.contact@bosch.com",
    license="Apache License",
    Requires="Python>=3.6, and pip >= 19.0",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent"
    ],
    packages= find_packages(),
    include_package_data=True,
    install_requires=["requests"]
)
