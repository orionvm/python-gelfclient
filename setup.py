import os
from setuptools import setup

try:
    from pypandoc import convert
    read_md = lambda f: convert(f, 'rst')    
except ImportError:
    print("warning: pypandoc module not found, could not convert Markdown to RST")
    read_md = lambda f: open(f, 'r').read()

from pygelf import __version__
setup(
    name = "pygelf",
    version = __version__,
    author = "Chris McClymont",
    author_email = "chris@mcclymont.it",
    description = "A UDP client for sending message in the Graylog Extended Log Format (GELF)",
    license = "Apache v2",
    keywords = "gelf, graylog, graylog2, logging",
    url = "http://github.com/orionvm/pygelf",
    packages = ['pygelf'],
    long_description=read_md('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "Topic :: System :: Logging"
    ],
)
