from unittest import IsolatedAsyncioTestCase
from .awss3foldertestcase import AWSS3FolderTestCase
from heaserver.service.db import awsservicelib
from heaserver.service.db.aws import S3
import boto3
from botocore.exceptions import ClientError
from freezegun.api import FakeDatetime
from dateutil.tz import tzutc
from heaobject.user import NONE_USER
from moto import mock_sts


class TestS3GetAccount(IsolatedAsyncioTestCase):

    @mock_sts()
    def run(self, result):
        super().run(result)

    async def test_get_account(self):
        sts = boto3.client('sts')
        actual = await S3._get_account(sts, NONE_USER)
        self.assertEquals('123456789012', actual.id)


class TestAWSServiceLib(AWSS3FolderTestCase):

    @mock_sts()
    def run(self, result):
        super().run(result)

    async def test_get_property(self):
        async with self.client.request('GET', '/properties/CLOUD_AWS_CRED_URL') as resp:
            self.assertEquals(200, resp.status)

    async def test_get_property_not_found(self):
        async with self.client.request('GET', '/properties/TEST') as resp:
            self.assertEquals(404, resp.status)

    async def test_get_volume_id_for_account_id(self):
        async with self.client.request('GET', '/accounts/123456789012') as resp:
            self.assertEquals(200, resp.status)

    async def test_list_bucket_not_found(self):
        s3 = boto3.client('s3')
        with self.assertRaises(ClientError):
            l = [o async for o in awsservicelib.list_objects(s3, 'blah')]

    async def test_list_bucket(self):
        s3 = boto3.client('s3')
        expected = [{'Key': 'TestFolder/', 'LastModified': FakeDatetime(2022, 5, 17, 0, 0, tzinfo=tzutc()),
                     'ETag': '"d41d8cd98f00b204e9800998ecf8427e"', 'Size': 0, 'StorageClass': 'STANDARD'},
                    {'Key': 'TestFolder2/', 'LastModified': FakeDatetime(2022, 5, 17, 0, 0, tzinfo=tzutc()),
                     'ETag': '"d41d8cd98f00b204e9800998ecf8427e"', 'Size': 0, 'StorageClass': 'STANDARD'}]
        actual = [o async for o in awsservicelib.list_objects(s3, 'arp-scale-2-cloud-bucket-with-tags11')]
        self.assertEquals(expected, actual)

    async def test_list_empty_bucket_with_filter(self):
        s3 = boto3.client('s3')
        expected = [{'Key': 'TestFolder/', 'LastModified': FakeDatetime(2022, 5, 17, 0, 0, tzinfo=tzutc()),
                     'ETag': '"d41d8cd98f00b204e9800998ecf8427e"', 'Size': 0, 'StorageClass': 'STANDARD'},
                    {'Key': 'TestFolder2/', 'LastModified': FakeDatetime(2022, 5, 17, 0, 0, tzinfo=tzutc()),
                     'ETag': '"d41d8cd98f00b204e9800998ecf8427e"', 'Size': 0, 'StorageClass': 'STANDARD'}]
        actual = [o async for o in
                  awsservicelib.list_objects(s3, 'arp-scale-2-cloud-bucket-with-tags11', prefix='TestFolder')]
        self.assertEquals(expected, actual)

    async def test_list_empty_bucket_with_filter_one(self):
        s3 = boto3.client('s3')
        expected = [{'Key': 'TestFolder/', 'LastModified': FakeDatetime(2022, 5, 17, 0, 0, tzinfo=tzutc()),
                     'ETag': '"d41d8cd98f00b204e9800998ecf8427e"', 'Size': 0, 'StorageClass': 'STANDARD'}]
        actual = [o async for o in
                  awsservicelib.list_objects(s3, 'arp-scale-2-cloud-bucket-with-tags11', prefix='TestFolder/')]
        self.assertEquals(expected, actual)

    async def test_delete_object(self):
        s3 = boto3.client('s3')
        actual = await awsservicelib._delete_object(s3, bucket_name='arp-scale-2-cloud-bucket-with-tags11',
                                                    key='TestFolder2/', recursive=True)
        self.assertEquals(204, actual.status)

    async def test_delete_object_not_found(self):
        s3 = boto3.client('s3')
        actual = await awsservicelib._delete_object(s3, bucket_name='arp-scale-2-cloud-bucket-with-tags11',
                                                    key='foobar/', recursive=True)
        self.assertEquals(404, actual.status)

    async def test_delete_object_bucket_not_found(self):
        s3 = boto3.client('s3')
        actual = await awsservicelib._delete_object(s3, bucket_name='arp-scale-2-cloud-bucket-with-tags1',
                                                    key='TestFolder2/', recursive=True)
        self.assertEquals(404, actual.status)

    async def test_copy_object(self):
        s3 = boto3.client('s3')
        actual = await awsservicelib._copy_object(s3, source_bucket_name='arp-scale-2-cloud-bucket-with-tags11',
                                                  source_key_name='TestFolder2/',
                                                  destination_bucket_name='arp-scale-2-cloud-bucket-with-tags11',
                                                  destination_key_name='foobar/TestFolder3/')
        self.assertEquals(201, actual.status)

    async def test_copy_object_not_found_source_bucket(self):
        s3 = boto3.client('s3')
        actual = await awsservicelib._copy_object(s3, source_bucket_name='arp-scale-2-cloud-bucket-with-tags1',
                                                  source_key_name='TestFolder2/',
                                                  destination_bucket_name='arp-scale-2-cloud-bucket-with-tags11',
                                                  destination_key_name='foobar/TestFolder3/')
        self.assertEquals(400, actual.status)

    async def test_copy_object_not_found_destination_bucket(self):
        s3 = boto3.client('s3')
        actual = await awsservicelib._copy_object(s3, source_bucket_name='arp-scale-2-cloud-bucket-with-tags11',
                                                  source_key_name='TestFolder2/',
                                                  destination_bucket_name='arp-scale-2-cloud-bucket-with-tags1',
                                                  destination_key_name='foobar/TestFolder3/')
        self.assertEquals(400, actual.status)

    async def test_copy_object_not_found_object(self):
        s3 = boto3.client('s3')
        actual = await awsservicelib._copy_object(s3, source_bucket_name='arp-scale-2-cloud-bucket-with-tags11',
                                                  source_key_name='TestFolder22/',
                                                  destination_bucket_name='arp-scale-2-cloud-bucket-with-tags11',
                                                  destination_key_name='foobar/TestFolder3/')
        self.assertEquals(400, actual.status)
