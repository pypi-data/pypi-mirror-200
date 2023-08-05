from setuptools import setup, find_packages

DISTNAME = "quest_eras"
VERSION = "1.6.4.3"
EXTENSIONS = []
PYTHON_REQUIRES = ">=3.8"
DESCRIPTION = "Sandia National Laboratories application suite for energy storage analysis and evaluation tools."
LONG_DESCRIPTION = "Sandia National Laboratories application suite for energy storage analysis and evaluation tools."
AUTHOR = "Sandia National Laboratories"
MAINTAINER_EMAIL = "tunguy@sandia.gov"
LICENSE = "BSD 3-clause"
URL = "https://www.github.com/snl-quest/snl-quest"

setuptools_kwargs = {
    "scripts": [],
    "include_package_data": True,
    "install_requires": [
        "numpy",
        "scipy",
        "pandas>=0.24.2",
        "pyomo>=5.6",
        "matplotlib>=3.5.1",
        "kivy>=1.10.1",
        "kivy-garden",
        "xlrd",
        "six",
        "jinja2",
        "bs4",
        "requests",
        "urllib3",
        "holidays",
        "seaborn",
        "eppy",
        "openpyxl",
        "pyutilib",
    ],
}

setup(
    name=DISTNAME,
    version=VERSION,
    packages=find_packages() + ['.'],
    ext_modules=EXTENSIONS,
    python_requires=PYTHON_REQUIRES,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    author=AUTHOR,
    entry_points = {'gui_scripts': ['quest = quest_eras.main:QuESt_App']} ,
    maintainer_email=MAINTAINER_EMAIL,
    license=LICENSE,
    url=URL,
    **setuptools_kwargs
)
