import unittest
from heaserver.service.db import awss3bucketobjectkey


class BucketObjectKeyTest(unittest.TestCase):
    def test_replace_parent_folder(self):
        self.assertEqual('baz/bar', awss3bucketobjectkey.replace_parent_folder('foo/oof/bar', 'baz/bar'))


# joined, split
split_join_data = [
    ('hello/goodbye/foobar/', ('hello/goodbye/', 'foobar/')),
    ('hello/goodbye/foobar', ('hello/goodbye/', 'foobar')),
    ('foobar', ('', 'foobar')),
    ('/', ('', '/'))
]


def join_test_generator(joined, split):
    def test(self):
        self.assertEquals(joined, awss3bucketobjectkey.join(*split))
    return test


def split_test_generator(joined, split):
    def test(self):
        self.assertEquals(split, awss3bucketobjectkey.split(joined))
    return test


for d in split_join_data:
    join_test = join_test_generator(d[0], d[1])
    setattr(BucketObjectKeyTest, f'test_join_{d[1]}', join_test)
    split_test = split_test_generator(d[0], d[1])
    setattr(BucketObjectKeyTest, f'test_split_{d[0]}', split_test)


# original, encoded, is_folder
encode_decode_data = [('foobar', 'Zm9vYmFy', False),
                      ('foobar/', 'Zm9vYmFyLw==', True),
                      ('hello/goodbye/foobar/', 'aGVsbG8vZ29vZGJ5ZS9mb29iYXIv', True)]


def encode_test_generator(orig, encoded):
    def test(self):
        self.assertEquals(encoded, awss3bucketobjectkey.encode_key(orig))
    return test


def decode_test_generator(orig, encoded):
    def test(self):
        self.assertEquals(orig, awss3bucketobjectkey.decode_key(encoded))
    return test


def is_folder_test_generator(orig, is_folder):
    def test(self):
        self.assertEqual(is_folder, awss3bucketobjectkey.is_folder(orig))
    return test


for d in encode_decode_data:
    join_test = encode_test_generator(d[0], d[1])
    setattr(BucketObjectKeyTest, f'test_encode_{d[0]}', join_test)
    split_test = decode_test_generator(d[0], d[1])
    setattr(BucketObjectKeyTest, f'test_decode_{d[0]}', split_test)
    is_folder_test = is_folder_test_generator(d[0], d[2])
    setattr(BucketObjectKeyTest, f'test_is_folder_{d[0]}', is_folder_test)

