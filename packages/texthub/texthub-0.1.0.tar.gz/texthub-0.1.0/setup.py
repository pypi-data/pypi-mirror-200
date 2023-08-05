import setuptools
from texthub import __version__

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="texthub",
    version=__version__,
    author="owo",
    author_email="contact@owomail.cc",
    description="A Python library that provides a simple interface to use NLP models",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Keycatowo/text-hub",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "pandas",
        "bidict",
        "transformers",
        "torch"
    ],
)