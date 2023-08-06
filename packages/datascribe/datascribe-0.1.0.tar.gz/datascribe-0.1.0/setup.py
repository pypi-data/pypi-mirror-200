from setuptools import setup, find_packages
import codecs
import os


VERSION = '0.1.0'
DESCRIPTION = 'A package that allows the user to record dataset metainfo in excel'
LONG_DESCRIPTION = 'A package that allows the user to record, document, organize the metadata of the dataset in an excel sheet'

# Setting up
setup(
    name="datascribe",
    version=VERSION,
    author="Jaswanth",
    author_email="kjswnth@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['openpyxl', 'datetime', 'pandas'],
    keywords=['python', 'dataset', 'url', 'record', 'excel', 'organize'],
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
    ]
)