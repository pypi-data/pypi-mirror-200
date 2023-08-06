from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'Twitter Only Here'
LONG_DESCRIPTION = 'A package to scrape twitter data easily'

# Setting up
setup(
    name="nimbus_twitter",
    version=VERSION,
    author="nimbusnext (Atharv Patawar)",
    author_email="<mail@neuralnine.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['snscrape', 'pandas'],
    keywords=['python', 'twitter', 'scrape'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)