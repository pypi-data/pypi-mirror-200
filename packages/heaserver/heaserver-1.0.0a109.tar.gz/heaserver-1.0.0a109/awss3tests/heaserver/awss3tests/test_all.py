from unittest import TestCase
from heaserver.service.db import awsservicelib
from botocore.exceptions import ClientError


class TestAWSServiceLib(TestCase):
    def test_key_in_folder(self):
        self.assertTrue(awsservicelib.key_in_folder('foo/bar/baz', 'foo/bar/'))

    def test_key_in_non_folder(self):
        self.assertFalse(awsservicelib.key_in_folder('foo/bar/baz', 'foo/bar'))

    def test_key_not_in_folder(self):
        self.assertFalse(awsservicelib.key_in_folder('foo/bar', 'foo/bar/baz/'))

    def test_decode_folder_root(self):
        self.assertEqual('', awsservicelib.decode_folder('root'))

    def test_decode_folder_non_root(self):
        self.assertEqual('/', awsservicelib.decode_folder('Lw=='))

    def test_decode_not_folder(self):
        self.assertEqual(None, awsservicelib.decode_folder('VGV4dEZpbGUucGRm'))

    def test_handle_client_error_404(self):
        c = ClientError(error_response={'Error': {'Code': awsservicelib.CLIENT_ERROR_404}}, operation_name='foo')
        self.assertEqual(404, awsservicelib.handle_client_error(c).status)

    def test_handle_client_error_no_such_bucket(self):
        c = ClientError(error_response={'Error': {'Code': awsservicelib.CLIENT_ERROR_NO_SUCH_BUCKET}}, operation_name='foo')
        self.assertEqual(404, awsservicelib.handle_client_error(c).status)

    def test_handle_client_error_unknown(self):
        c = ClientError(error_response={'Error': {'Code': "It's wrecked"}},
                        operation_name='foo')
        self.assertEqual(500, awsservicelib.handle_client_error(c).status)


