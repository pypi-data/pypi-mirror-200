from setuptools import setup, find_packages
import os


VERSION = '0.0.2'
DESCRIPTION = 'First one for test'
LONG_DESCRIPTION = 'A long description for nothing'

# Setting up
setup(
    name="testroger",
    version=VERSION,
    author="Florian",
    author_email="<mail@mail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=[],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)