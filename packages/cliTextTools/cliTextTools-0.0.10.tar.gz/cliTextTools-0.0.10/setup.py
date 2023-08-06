from setuptools import setup, find_packages
import os

VERSION = '0.0.10'
DESCRIPTION = 'Text tools for cli based progams'
LONG_DESCRIPTION = 'tools like typing print and user input control'


setup(
    name="cliTextTools",
    version=VERSION,
    author="rosejustin601 (Justin Rose)",
    author_email="rosejustin601@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'cli', 'text' 'tools'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Environment :: Console",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English"
    ]
)
