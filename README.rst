========================
Snowflake Design Pattern
========================

.. image:: http://img.shields.io/travis/Midnighter/snowflake/master.png
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/Midnighter/snowflake

.. image:: http://img.shields.io/coveralls/Midnighter/snowflake/master.png
    :alt: Coverage Status
    :target: https://coveralls.io/r/Midnighter/snowflake

.. image:: http://img.shields.io/pypi/v/snowflake.png
    :alt: PYPI Package
    :target: https://pypi.python.org/pypi/snowflake


    Listen up, maggots. You are not special. You are not a beautiful or unique snowflake. You're the same decaying organic matter as everything else.

    -- Fight Club by Chuck Palahniuk

The Python module ``snowflake.py`` provides a class ``Snowflake`` that stores
existing instances of its type and identifies them by a given ID. Subsequent
attempts to create instances with the same ID simply yield the known object
without updating its attributes.

* Any class inheriting from ``Snowflake`` and appropriately calling its
  ``__init__`` method will follow this behaviour.
* Instantiation is currently not thread safe, though it should be fairly easy to
  do so, since it already uses a metaclass.
* Objects of this type are fully pickleable.

Use Case
--------

The idea for this design pattern comes from a need in bioinformatics to track
unique and (mostly) invariable entities across different container structures. A
gene, for example, may be part of a chromosome, a signalling pathway, and a
regulatory network. Having a unique description of that gene and being able to
identify the unique instance of that gene in all organisational structures
seemed "the right thing to do".

License
-------

Please refer to the separate file ``LICENSE.rst``.

Examples
--------

In a first step you probably want to define a class that inherits from
``Snowflake``. This class uses ``super`` and accepts keyword arguments
and can thus be used in multiple inheritance.

Note
~~~~

Classes that inherit from ``Snowflake`` should always be initialised with
keyword arguments.

.. code:: python

    from snowflake import Snowflake

    class Gene(Snowflake):

        def __init__(self, unique_id, common_name, sequence=None, **kw_args):
            super(Gene, self).__init__(unique_id=unique_id, **kw_args)
            self.name = common_name
            self.seq = sequence

It is then possible to use this class in the following ways

.. code:: python

    >>> a = Gene(unique_id=3245, common_name="rcsB")
    >>> b = Gene(unique_id=3245, common_name="tomfoolery", sequence="AATT")
    >>> a == b
    True
    >>> b.name
    'rcsB'
    >>> b.seq

Installation
------------

.. code:: bash

    pip install snowflake

Documentation
-------------

https://snowflake.readthedocs.org/

Development
-----------

To run the all tests run

.. code:: bash

    tox

or, in parallel

.. code:: bash

    detox
