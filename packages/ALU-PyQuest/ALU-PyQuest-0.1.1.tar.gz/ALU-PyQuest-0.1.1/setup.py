from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.1.1'
DESCRIPTION = 'Python Programming quiz'

def get_long_description():
    """
    Return the README.
    """
    return open("README.md", "r", encoding="utf8").read()

# Setting up
setup(
    name="ALU-PyQuest",
    version=VERSION,
    url="https://github.com/Elhameed/ALU-PYQUEST",
    license="MIT",
    description=DESCRIPTION,
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Teniola Ajani",
    author_email="a.ajani@alustudent.com",
    packages=find_packages(),
    python_requires=">=3.7",
    include_package_data=True,
    install_requires=[''],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    scripts=['quiz.py'],
    entry_points={
    'console_scripts': [
        'PyQuest=quiz:playgame'
    ]
},
    project_urls={
        "Source": "https://github.com/Elhameed/ALU-PYQUEST",
    },
)

