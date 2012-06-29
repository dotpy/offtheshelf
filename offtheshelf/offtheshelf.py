"""Simple NoSQL database using the shelve module as backend."""


import os
import shelve
import pickle
import fcntl


__all__ = ["Database",
           "Collection",
           "openDB"]


class Collection(object):
    """A list of dictionaries (documents) accessible in a DB-like way."""

    def __init__(self, name):
        """Initialize empty collection identified by 'name'."""
        self.name = name
        self._docs = []

    def insert(self, values):
        """Add a new document to the collection."""
        assert isinstance(values, dict), "values is not a dictionary"
        self._docs.append(values)

    def update(self, values, where={}):
        """Update matching doc(s) with the values provided."""
        for d in self.find(where):
            d.update(values)

    def upsert(self, values, where={}):
        """Update matching docs or insert values if no matching doc is found."""
        self.update(values, where) if self.count(where) else self.insert(values)

    def delete(self, where):
        """Delete matching doc(s) from the collection."""
        self._docs = [d for d in self._docs if not self._match(d, where)]

    def truncate(self):
        """Truncate the collection."""
        self._docs = []

    def find(self, where={}):
        """Return matching doc(s)."""
        return [d for d in self._docs if self._match(d, where)]

    def find_one(self, where={}):
        """Return the first matching doc."""
        try:
            return self.find(where)[0]
        except IndexError:
            return None

    def count(self, where={}):
        """Return the number of matching docs."""
        return len(self.find(where))

    def _match(self, doc, where):
        """Return True if 'doc' matches the 'where' condition."""
        assert isinstance(where, dict), "where is not a dictionary"
        try:
            return all([doc[k] == v for k, v in where.items()])
        except KeyError:
            return False

    def __str__(self):
        return "{!s}".format(self._docs)


class Database(object):
    """Dictionary-like object containing one or more named collections."""

    def __init__(self, filename, protocol=pickle.HIGHEST_PROTOCOL,
                 writeback=True, collection=Collection, use_lock=True):
        """Initialize the underlying database.

        'filename' is the path of the DB file (without trailing '.db')
        'protocol' is the version of pickle protocol to use
        'writeback' enables write-back of open collections on db close
        'collection' allows you to provide a custom collection class
        'lock' enables use of lock file to manage concurrent access to database
        """
        self._collection_type = collection
        self.lock = None

        if use_lock:
            self.lock = open("{}.lck".format(filename), "w")
            fcntl.flock(self.lock, fcntl.LOCK_EX)

        self._dict = shelve.open(filename, "c", protocol, writeback)

    def get_collection(self, name="__default__", *args):
        """Create a collection (if new) in the DB and return it.

        Additional arguments are directly passed to the collection.
        """
        if not name in self._dict:
            self._dict[name] = self._collection_type(name, *args)
        return self._dict[name]

    def drop_collection(self, name="__default__"):
        """Drop the specified collection from the database."""
        return self._dict.pop(name)

    @property
    def collections(self):
        """Return the collections in the database."""
        return self._dict

    def save(self):
        """Dump data to file."""
        self._dict.sync()

    def close(self):
        """Save file and release lock (if locking is enabled)."""
        self._dict.close()
        if self.lock is not None:
            fcntl.flock(self.lock, fcntl.LOCK_UN)
            self.lock.close()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    def __str__(self):
        return "{!s}".format(self._dict)


def openDB(*args, **kwargs):
    """Return an open Database (for use with closures)."""
    return Database(*args, **kwargs)
