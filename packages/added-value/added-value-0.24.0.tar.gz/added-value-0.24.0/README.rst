===========
Added Value
===========

A Sphinx extension for embedding Python object *values* into documentation as text, lists
or tables.

This is achieved by adding new roles and directives which refer to Python objects which contain
the values to be represented. The extension provides roles for embedded single and lists of values,
and a sophisticated directive for rendering complex data structures like lists of dictionaries as
tables.


Status
======

Build status:

.. image:: https://github.com/sixty-north/added-value/workflows/CI/badge.svg?branch=master
     :target: https://github.com/sixty-north/added-value/actions?workflow=CI
     :alt: CI Status

.. image:: https://readthedocs.org/projects/added-value/badge/?version=latest
    :target: https://added-value.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status


Installation
============

The ``added-value`` package is available on the Python Package Index (PyPI):

.. image:: https://badge.fury.io/py/added-value.svg
    :target: https://badge.fury.io/py/added-value

The package supports Python 3 only. To install::

  $ pip install added-value


Usage
=====

*Added Value* provides a number of roles and directives for embedding Python values into your
documentation. For example, sing added value we can extract the value of *pi* from the Python
Standard Library ``math`` module, and embed it in a sentence, using the ``format`` role provided
by *Added Values*, like this:

::

    The ratio of the circumference to the diameter of a circle is :format:`math.pi, .3f` to three
    decimal places.

Which gives:

    The ratio of the circumference to the diameter of a circle is 3.142 to three
    decimal places.

Powerful tools
--------------

Added value is powerful, and allows lists, dictionaries, and even complex data structures such as
lists of lists of dictionaries to be rendered into tables in various ways. Consult the
`documentation <https://added-value.readthedocs.io/en/latest/>`_ for more details.

