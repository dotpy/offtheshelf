offtheshelf
===========

`offtheshelf` is a pure-Python module providing a very simple and minimalist
embedded NoSQL database. It uses the `shelve` module as backend for persistent
storage and relies on file-locking as a simple mutual exclusion mechanism.

It has no dependencies and runs on both Python 2.x and 3.x.


Installation
------------
Download the source code from [GitHub](https://github.com/dotpy/offtheshelf)
and run the install script:

    # python setup.py install


Basic usage
-----------
`offtheshelf` defines two classes: `Database` and `Collection`.

A `Database` class is basically a container for one or more `Collection`s. A
`Collection` contains a list of documents (i.e. dictionaries), holding the
actual data, and provides methods for inserting, updating, searching and
removing items from documents.

`Database` instances support closures and can be either returned by a call to
the `openDB()` function or instantiated directly; e.g.:

    >>> with offtheshelf.openDB("/tmp/music") as db:
    ...     coll = db.get_collection("CDCollection")
    ...     coll.insert({"Author": "W. A. Mozart",
    ...                  "Title":  "Symphony K.551 - Jupiter"})
    ...     coll.insert({"Author": "L. Van Beethoven",
    ...                  "Title":  "Symphony n.5 op.67"})

`Collection`s can be queried, updated, counted and deleted; e.g.:

    ...     coll.count({"Author": "L. Van Beethoven"})
    1
    ...     coll.find({"Author": "W. A. Mozart"})
    [{'Author': 'W. A. Mozart', 'Title': 'Symphony K.551 - Jupiter'}]
    ...     # Don't worry Ludwig, it's only an example! :-(
    ...     coll.delete({"Author": "L. Van Beethoven"})
    ...

The `Database` is automatically saved and closed upon exit from the closure,
but can be also explicitely saved and closed; e.g.:

    >>> db = Database("/tmp/music")
    >>> coll = db.get_collection("CDCollection")
    >>> coll.update({"Genre": "Classical"})
    >>> db.save()
    >>> db.close()


Documentation
-------------
More examples and a detailed description of the module and its classes are
available at http://www.kernel-panic.it/programming/offtheshelf/.


Tests
-----
To run the test suite, just run `python setup.py test`.


Credits
-------
Copyright (c) 2012 Daniele Mazzocchio (danix@kernel-panic.it).

Licensed under BSD license (see LICENSE.md file).
