"""Test suite for the PacketFilter class"""

import unittest
import tempfile
import os.path

import offtheshelf


# Documents used for testing
TEST_DOC1 = {"key1": 1,  "key2": "value2"}
TEST_DOC2 = {"key1": 10, "key2": "value20"}


class TestCollection(unittest.TestCase):
    """Test case class for offtheshelf.Collection"""

    def setUp(self):
        self._file = tempfile.NamedTemporaryFile(suffix=".db")
        self._db = offtheshelf.openDB(os.path.splitext(self._file.name)[0])
        self.collection = self._db.get_collection()
        self.collection.truncate()

    def tearDown(self):
        self._db.close()
        self._file.close()

    def test_insert(self):
        self.collection.insert(TEST_DOC1)
        self.assertEqual(self.collection.find_one(), TEST_DOC1)

    def test_update(self):
        self.collection.insert(TEST_DOC1)
        self.collection.update({"key1": 2}, {"key2": "nonexistent"})
        self.assertEqual(self.collection.find_one(), TEST_DOC1)
        self.collection.update({"key1": 2})
        self.assertEqual(self.collection.find_one()["key1"], 2)

    def test_upsert(self):
        self.collection.upsert(TEST_DOC1)
        self.assertEqual(self.collection.find_one(), TEST_DOC1)
        self.collection.upsert(TEST_DOC2, TEST_DOC1)
        self.assertEqual(self.collection.find_one(), TEST_DOC2)

    def test_delete(self):
        self.collection.insert(TEST_DOC1)
        self.collection.insert(TEST_DOC2)
        self.collection.delete({"key1": 10})
        self.assertEqual(self.collection.count(), 1)
        self.collection.insert(TEST_DOC2)

    def test_truncate(self):
        self.collection.insert(TEST_DOC1)
        self.collection.insert(TEST_DOC2)
        self.collection.truncate()
        self.assertEqual(self.collection.count(), 0)

    def test_find(self):
        self.collection.insert(TEST_DOC1)
        self.collection.insert(TEST_DOC2)
        self.assertEqual(len(self.collection.find()), 2)
        self.assertEqual(len(self.collection.find({"key1": 1})), 1)

    def test_find_one(self):
        self.collection.insert(TEST_DOC1)
        self.assertEqual(self.collection.find_one(), TEST_DOC1)

    def test_count(self):
        self.collection.insert(TEST_DOC1)
        self.collection.insert(TEST_DOC2)
        self.assertEqual(self.collection.count(), 2)
        self.assertEqual(self.collection.count({"key1": 1}), 1)
        self.assertEqual(self.collection.count({"key1": 2}), 0)
        self.collection.insert(TEST_DOC1)
        self.assertEqual(self.collection.count({"key1": 1}), 2)
