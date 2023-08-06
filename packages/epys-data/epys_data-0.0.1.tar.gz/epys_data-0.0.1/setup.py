from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = "A python library created to extract data from EPİAŞ's epys services."

# Setting up
setup(
    name="epys_data",
    version=VERSION,
    author="Berkay Akpınar",
    author_email="<brky45@gmail.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['pandas', 'requests', 'numpy'],
    keywords=['python', 'epys', 'epias', 'enerji piyasaları', 'data'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)