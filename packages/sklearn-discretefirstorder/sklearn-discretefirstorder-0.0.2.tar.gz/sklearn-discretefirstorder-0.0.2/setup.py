#! /usr/bin/env python
"""A scikit-learn compatible discrete first-order method
for subset selection."""

import codecs
import os

from setuptools import find_packages, setup

# get __version__ from _version.py
ver_file = os.path.join("discretefirstorder", "_version.py")
with open(ver_file) as f:
    exec(f.read())

DISTNAME = "sklearn-discretefirstorder"
DESCRIPTION = "A scikit-learn compatible discrete first-order method for subset selection."
with codecs.open("README.rst", encoding="utf-8-sig") as f:
    LONG_DESCRIPTION = f.read()
MAINTAINER = "M. Fernandez-Montes"
MAINTAINER_EMAIL = "miguel_fmontes@berkeley.edu"
URL = ""
LICENSE = "new BSD"
DOWNLOAD_URL = ""
VERSION = __version__
INSTALL_REQUIRES = ["numpy", "scipy", "scikit-learn"]
CLASSIFIERS = [
    "Intended Audience :: Science/Research",
    "Intended Audience :: Developers",
    "License :: OSI Approved",
    "Programming Language :: Python",
    "Topic :: Software Development",
    "Topic :: Scientific/Engineering",
    "Operating System :: Microsoft :: Windows",
    "Operating System :: POSIX",
    "Operating System :: Unix",
    "Operating System :: MacOS",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
]
EXTRAS_REQUIRE = {
    "tests": ["pytest", "pytest-cov"],
    "docs": [
        "sphinx",
        "sphinx-gallery",
        "sphinx_rtd_theme",
        "numpydoc",
        "matplotlib",
        "pillow",
    ],
}

setup(
    name=DISTNAME,
    maintainer=MAINTAINER,
    maintainer_email=MAINTAINER_EMAIL,
    description=DESCRIPTION,
    license=LICENSE,
    url=URL,
    version=VERSION,
    download_url=DOWNLOAD_URL,
    long_description=LONG_DESCRIPTION,
    zip_safe=False,  # the package can run out of an .egg file
    classifiers=CLASSIFIERS,
    packages=find_packages(),
    install_requires=INSTALL_REQUIRES,
    extras_require=EXTRAS_REQUIRE,
    python_requires=">=3.5",
)
