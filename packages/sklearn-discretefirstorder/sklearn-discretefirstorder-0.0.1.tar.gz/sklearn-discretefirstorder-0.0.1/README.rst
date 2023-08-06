.. -*- mode: rst -*-

|ReadTheDocs|_ |Maintenance yes|

.. |ReadTheDocs| image:: https://readthedocs.org/projects/sklearn-firstordersubset/badge/?version=latest
.. _ReadTheDocs: https://sklearn-firstordersubset.readthedocs.io/en/latest/?badge=latest

.. |Maintenance yes| image:: https://img.shields.io/badge/Maintained%3F-yes-green.svg
   :target: https://github.com/miguelfmc/sklearn-discretefirstorder/commit-activity

A Discrete First Order Method for Subset Selection
==================================================

.. _scikit-learn: https://scikit-learn.org
.. _documentation: https://sklearn-discretefirstorder.readthedocs.io/en/latest/quick_start.html

**sklearn-discretefirstorder** is a light-weight package that implements a simple
discrete first-order method for best feature subset selection in linear regression.

The discrete first-order method is based on the technique described by Berstimas et al. [1]_

The package is built on top of the scikit-learn_ framework and is compatible with scikit-learn methods
such as cross-validation and pipelines.
I followed the guidelines for developing scikit-learn estimators
as outlined in the `scikit-learn documentation <https://scikit-learn.org/stable/developers/develop.html>`_.

About the project
-----------------
I created this project first and foremost to learn more about how to build and maintain a Python project.
My goal was never to build a state-of-the-art machine learning package.

I picked this topic because I had experimented with different feature selection approaches
(including the discrete first-order method implemented here) as part of a grad school class project.
However, I never developed a robust, well-documented codebase. I decided to re-implement the simplest technique from my grad school project so that I could focus on 
key aspects of project development such as proper API design, documentation and testing.

I felt like the scikit-learn framework was appropriate for this ML use-case and, more generally, a good set of guiding principles
for my first proper Python package thanks to its clear standards and good documentation.

At the moment, the project is in a very early stage of development, but basic usage is already possible.
If time permits, I plan to add more features and improve the documentation.

Installation
------------

To install the package, clone this repo and run ``pip install``::
   
   git clone https://github.com/miguelfmc/sklearn-discretefirstorder
   cd sklearn-discretefirstorder
   pip install .

Quick Start
-----------

Once you have installed the package you can start using it as follows:

The key estimator in this packages is the ``discretefirstorder.DFORegressor``.
You can import it as::

   from discretefirstorder import DFORegressor

Easily fit the estimator as follows::

   import numpy as np
   from discretefirstorder import DFORegressor
   X = np.arange(100).reshape(100, 1)
   y = np.random.normal(size=(100, ))
   estimator = DFORegressor()
   estimator.fit(X, y)

For more examples, see the documentation_.

Known Issues
------------
This package is still at a very early stage of development. The following issues are known:

* Optimization routines are implemented in Python, which makes them slow.
* At the moment, the package only supports squared error loss minimization but there are plans to include support for absolute error loss minimization.
* At the moment, there is no support for classification problems i.e. logistic regression.
* I'm working on making the package available on PyPI and conda-forge. Stay tuned for updates!

Contributing
------------
While the project is still in its early stages, contributions are welcome!

To contribute, please fork the repo and clone it to your local machine. Then, create a new branch and make your changes.

I suggest you set-up your local environment with conda and pip::
   
      conda create -n sklearn-discretefirstorder python=3.8
      conda activate sklearn-discretefirstorder
      pip install -r requirements.txt -r requirements-dev.txt -r requirements-docs.txt -r requirements-test.txt

You can also use conda to install all the dependencies from the ``environment.yml`` file::

      conda env create -f environment.yml
      conda activate sklearn-discretefirstorder
   
Then, install the package in editable mode::
   
      pip install -e .

License
-------
Distributed under BSD 3-Clause License. See ``LICENSE`` for more information.

References
----------
.. [1] Dimitris Bertsimas. Angela King. Rahul Mazumder. "Best subset selection via a modern optimization lens." Ann. Statist. 44 (2) 813 - 852, April 2016. https://doi.org/10.1214/15-AOS1388 
