

from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.1.0.2'
DESCRIPTION = 'A collection of useful code "snippets"'
LONG_DESCRIPTION = 'A collection of useful code "snippets" or "helpers" that implement little but annoying to add things for you'

# Setting up
setup(
    name="einfach",
    version=VERSION,
    author="rotgruengelb (Daniel)",
    author_email="<code@rotgruengelb.net>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'helper', 'helpers', 'help', 'easy code', 'ease of use'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)