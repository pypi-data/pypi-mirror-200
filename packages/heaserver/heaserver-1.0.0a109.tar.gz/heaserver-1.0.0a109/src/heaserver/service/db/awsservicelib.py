"""
Functions for interacting with Amazon Web Services.

This module supports management of AWS accounts, S3 buckets, and objects in S3 buckets. It uses Amazon's boto3 library
behind the scenes.

In order for HEA to access AWS accounts, buckets, and objects, there must be a volume accessible to the user through
the volumes microservice with an AWSFileSystem for its file system. Additionally, credentials must either be stored
in the keychain microservice and associated with the volume through the volume's credential_id attribute,
or stored on the server's file system in a location searched by the AWS boto3 library. Users can only see the
accounts, buckets, and objects to which the provided AWS credentials allow access, and HEA may additionally restrict
the returned objects as documented in the functions below. The purpose of volumes in this case is to supply credentials
to AWS service calls. Support for boto3's built-in file system search for credentials is only provided for testing and
should not be used in a production setting. This module is designed to pass the current user's credentials to AWS3, not
to have application-wide credentials that everyone uses.

The request argument to these functions is expected to have a OIDC_CLAIM_sub header containing the user id for
permissions checking. No results will be returned if this header is not provided or is empty.

In general, there are two flavors of functions for getting accounts, buckets, and objects. The first expects the id
of a volume as described above. The second expects the id of an account, bucket, or bucket and object. The latter
attempts to match the request up to any volumes with an AWSFileSystem that the user has access to for the purpose of
determine what AWS credentials to use. They perform the
same except when the user has access to multiple such volumes, in which case supplying the volume id avoids a search
through the user's volumes.
"""
import asyncio
import logging
from concurrent.futures import ThreadPoolExecutor
from botocore.exceptions import ClientError
from aiohttp import web, hdrs

from .awss3bucketobjectkey import KeyDecodeException, decode_key, is_folder, join
from .. import response
from ..heaobjectsupport import PermissionGroup
from ..oidcclaimhdrs import SUB
from ..appproperty import HEA_DB
from ..uritemplate import tvars
from typing import Any, Optional, Callable, AsyncIterator
from collections.abc import Awaitable
from aiohttp.web import Request, Response, Application
from heaobject.volume import AWSFileSystem
from heaobject.user import NONE_USER, ALL_USERS
from heaobject.root import ShareImpl
from heaobject.folder import Folder
from heaobject.activity import Status, AWSActivity
from heaobject.aws import S3Version
from asyncio import gather, AbstractEventLoop
from functools import partial

from ..sources import HEA
from mypy_boto3_s3.client import S3Client

"""
Available functions
AWS object
- get_account
- post_account                    NOT TESTED
- put_account                     NOT TESTED
- delete_account                  CANT https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_accounts_close.html
                                  One solution would be to use beautiful soup : https://realpython.com/beautiful-soup-web-scraper-python/

- users/policies/roles : https://www.learnaws.org/2021/05/12/aws-iam-boto3-guide/

- change_storage_class            TODO
- copy_object
- delete_bucket_objects
- delete_bucket
- delete_folder
- delete_object
- download_object
- download_archive_object         TODO
- generate_presigned_url
- get_object_meta
- get_object_content
- get_all_buckets
- get all
- opener                          TODO -> return file format -> returning metadata containing list of links following collection + json format
-                                         need to pass back collection - json format with link with content type, so one or more links, most likely
- post_bucket
- post_folder
- post_object
- post_object_archive             TODO
- put_bucket
- put_folder
- put_object
- put_object_archive              TODO
- transfer_object_within_account
- transfer_object_between_account TODO
- rename_object
- update_bucket_policy            TODO

TO DO
- accounts?
"""
MONGODB_BUCKET_COLLECTION = 'buckets'

CLIENT_ERROR_NO_SUCH_BUCKET = 'NoSuchBucket'
CLIENT_ERROR_ACCESS_DENIED = 'AccessDenied'
CLIENT_ERROR_FORBIDDEN = '403'
CLIENT_ERROR_404 = '404'
CLIENT_ERROR_ALL_ACCESS_DISABLED = 'AllAccessDisabled'

ROOT_FOLDER = Folder()
ROOT_FOLDER.id = 'root'
ROOT_FOLDER.name = 'root'
ROOT_FOLDER.display_name = 'Root'
ROOT_FOLDER.description = "The root folder for an AWS S3 bucket's objects."
_root_share = ShareImpl()
_root_share.user = ALL_USERS
_root_share.permissions = PermissionGroup.POSTER_PERMS.perms
ROOT_FOLDER.shares = [_root_share]
ROOT_FOLDER.source = HEA


async def copy_object(request: Request) -> Response:
    """
    copy/paste (duplicate), throws error if destination exists, this so an overwrite isn't done
    throws another error is source doesn't exist
    https://medium.com/plusteam/move-and-rename-objects-within-an-s3-bucket-using-boto-3-58b164790b78
    https://stackoverflow.com/questions/47468148/how-to-copy-s3-object-from-one-bucket-to-another-using-python-boto3

    :param request: the aiohttp Request, with the body containing the target bucket and key, and the match_info
    containing the source volume, bucket, and key. (required).
    :return: the HTTP response.
    """
    logger = logging.getLogger(__name__)
    volume_id = request.match_info['volume_id']
    source_bucket_name = request.match_info['bucket_id']
    try:
        source_key_name = decode_key(request.match_info['id']) if 'id' in request.match_info else None
    except KeyDecodeException as e:
        return response.status_bad_request(str(e))
    if source_bucket_name is None or source_key_name is None:
        return response.status_bad_request(f'Invalid request URL')
    try:
        request_json = await request.json()
        destination_url = next(
            item['value'] for item in request_json['template']['data'] if item['name'] == 'target')
        destination_display_name = next(
            item['value'] for item in request_json['template']['data'] if item['name'] == 'display_name')
        if destination_display_name and destination_display_name.endswith('/'):
            return response.status_bad_request('THe name cannot end with a slash')
        vars_ = tvars(route='http{prefix}/volumes/{volume_id}/buckets/{bucket_id}/awss3folders/{id}',
                      url=destination_url)
        destination_bucket_name = vars_['bucket_id']
        destination_folder_name = decode_key(vars_['id']) if 'id' in vars_ else ''
        if destination_folder_name and not is_folder(destination_folder_name):
            return response.status_bad_request(f'Target property {destination_url} is not a folder')
        destination_key_name = join(destination_folder_name,
                                    destination_display_name) if destination_folder_name else destination_display_name
        if is_folder(source_key_name):
            destination_key_name += '/'
    except (KeyError, ValueError, KeyDecodeException) as e:
        logger.exception(f'Invalid destination')
        return response.status_bad_request(f'Invalid destination: {e}')
    logger.debug('Copy requested from %s/%s to %s/%s', source_bucket_name, source_key_name, destination_bucket_name,
                 destination_key_name)
    s3_client = await request.app[HEA_DB].get_client(request, 's3', volume_id)
    resp = await _copy_object(s3_client, source_bucket_name, source_key_name, destination_bucket_name,
                              destination_key_name)
    resp.headers[hdrs.LOCATION] = destination_url
    return resp


async def delete_object(request: Request, recursive=False,
                        activity_cb: Optional[
                            Callable[[Application, AWSActivity], Awaitable[None]]] = None) -> Response:
    """
    Deletes a single object. The volume id must be in the volume_id entry of the request's match_info dictionary. The
    bucket id must be in the bucket_id entry of the request's match_info dictionary. The item id must be in the id
    entry of the request's match_info dictionary. An optional folder id may be passed in the folder_id entry of the
    request's match_info_dictinary.

    :param request: the aiohttp Request (required).
    :param object_type: only delete the requested object only if it is a file or only if it is a folder. Pass in
    ObjectType.ANY or None (the default) to signify that it does not matter.
    :param recursive: if True, and the object is a folder, this function will delete the folder and all of its
    contents, otherwise it will return a 400 error if the folder is not empty. If the object to delete is not a folder,
    this flag will have no effect.
    :param activity_cb: optional coroutine that is called when potentially relevant activity occurred.
    :return: the HTTP response with a 204 status code if the item was successfully deleted, 403 if access was denied,
    404 if the item was not found, or 500 if an internal error occurred.
    """
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.delete_object
    # TODO: bucket.object_versions.filter(Prefix="myprefix/").delete()     add versioning option like in the delete bucket?
    if 'volume_id' not in request.match_info:
        return response.status_bad_request('volume_id is required')
    if 'bucket_id' not in request.match_info:
        return response.status_bad_request('bucket_id is required')
    if 'id' not in request.match_info:
        return response.status_bad_request('id is required')

    bucket_name = request.match_info['bucket_id']
    encoded_key = request.match_info['id']
    volume_id = request.match_info['volume_id']
    encoded_folder_key = request.match_info.get('folder_id', None)
    try:
        key: str | None = decode_key(encoded_key)
    except KeyDecodeException:
        return response.status_not_found()
    s3_client = await request.app[HEA_DB].get_client(request, 's3', volume_id)
    owner = request.headers.get(SUB, NONE_USER)
    folder_key = decode_folder(encoded_folder_key) if encoded_folder_key is not None else None
    if folder_key is not None and not key_in_folder(key, folder_key):
        loop = asyncio.get_running_loop()
        return await return_bucket_status_or_not_found(bucket_name, loop, s3_client)
    resp = await _delete_object(s3_client, bucket_name, key, recursive)
    if activity_cb:
        activity = AWSActivity()
        activity.owner = owner
        activity.user_id = activity.owner
        activity.status = Status.COMPLETE
        activity.action = f'Deleted {key}'
        if activity_cb:
            await activity_cb(request.app, activity)

    return resp


async def get_volume_id_for_account_id(request: web.Request) -> str | None:
    """
    Gets the id of the volume associated with an AWS account. The account id is expected to be in the request object's
    match_info mapping, with key 'id'.

    :param request: an aiohttp Request object (required).
    :return: a volume id string, or None if no volume was found associated with the AWS account.
    """
    print()
    async def get_one(request, volume_id):
        return volume_id, await request.app[HEA_DB].get_account(request, volume_id)

    return next((volume_id for (volume_id, a) in await gather(
        *[get_one(request, v.id) async for v in request.app[HEA_DB].get_volumes(request, AWSFileSystem)])
                 if
                 a.id == request.match_info['id']), None)



# def transfer_object_between_account():
#     """
#     https://markgituma.medium.com/copy-s3-bucket-objects-across-separate-aws-accounts-programmatically-323862d857ed
#     """
#     # TODO: use update_bucket_policy to set up "source" bucket policy correctly
#     """
#     {
#     "Version": "2012-10-17",
#     "Id": "Policy1546558291129",
#     "Statement": [
#         {
#             "Sid": "Stmt1546558287955",
#             "Effect": "Allow",
#             "Principal": {
#                 "AWS": "arn:aws:iam::<AWS_IAM_USER>"
#             },
#             "Action": [
#               "s3:ListBucket",
#               "s3:GetObject"
#             ],
#             "Resource": "arn:aws:s3:::<SOURCE_BUCKET>/",
#             "Resource": "arn:aws:s3:::<SOURCE_BUCKET>/*"
#         }
#     ]
#     }
#     """
#     # TODO: use update_bucket_policy to set up aws "destination" bucket policy
#     """
#     {
#     "Version": "2012-10-17",
#     "Id": "Policy22222222222",
#     "Statement": [
#         {
#             "Sid": "Stmt22222222222",
#             "Effect": "Allow",
#             "Principal": {
#                 "AWS": [
#                   "arn:aws:iam::<AWS_IAM_DESTINATION_USER>",
#                   "arn:aws:iam::<AWS_IAM_LAMBDA_ROLE>:role/
#                 ]
#             },
#             "Action": [
#                 "s3:ListBucket",
#                 "s3:PutObject",
#                 "s3:PutObjectAcl"
#             ],
#             "Resource": "arn:aws:s3:::<DESTINATION_BUCKET>/",
#             "Resource": "arn:aws:s3:::<DESTINATION_BUCKET>/*"
#         }
#     ]
#     }
#     """
#     # TODO: code
#     source_client = boto3.client('s3', "SOURCE_AWS_ACCESS_KEY_ID", "SOURCE_AWS_SECRET_ACCESS_KEY")
#     source_response = source_client.get_object(Bucket="SOURCE_BUCKET", Key="OBJECT_KEY")
#     destination_client = boto3.client('s3', "DESTINATION_AWS_ACCESS_KEY_ID", "DESTINATION_AWS_SECRET_ACCESS_KEY")
#     destination_client.upload_fileobj(source_response['Body'], "DESTINATION_BUCKET",
#                                       "FOLDER_LOCATION_IN_DESTINATION_BUCKET")


# async def rename_object(request: Request, volume_id: str, object_path: str, new_name: str):
#     """
#     BOTO3, the copy and rename is the same
#     https://medium.com/plusteam/move-and-rename-objects-within-an-s3-bucket-using-boto-3-58b164790b78
#     https://stackoverflow.com/questions/47468148/how-to-copy-s3-object-from-one-bucket-to-another-using-python-boto3
#
#     :param request: the aiohttp Request (required).
#     :param volume_id: the id string of the volume representing the user's AWS account.
#     :param object_path: (str) path to object, includes both bucket and key values
#     :param new_name: (str) value to rename the object as, will only replace the name not the path. Use transfer object for that
#     """
#     # TODO: check if ACL stays the same and check existence
#     try:
#         s3_resource = await request.app[HEA_DB].get_resource(request, 's3', volume_id)
#         copy_source = {'Bucket': object_path.partition("/")[0], 'Key': object_path.partition("/")[2]}
#         bucket_name = object_path.partition("/")[0]
#         old_name = object_path.rpartition("/")[2]
#         s3_resource.meta.client.copy(copy_source, bucket_name,
#                                      object_path.partition("/")[2].replace(old_name, new_name))
#     except ClientError as e:
#         logging.error(e)


def handle_client_error(e: ClientError) -> Response:
    logger = logging.getLogger(__name__)
    error_code = e.response['Error']['Code']
    if error_code in (CLIENT_ERROR_404, CLIENT_ERROR_NO_SUCH_BUCKET):  # folder doesn't exist
        logger.debug('Error from boto3: %s', exc_info=True)
        return response.status_not_found()
    elif error_code in (CLIENT_ERROR_ACCESS_DENIED, CLIENT_ERROR_FORBIDDEN, CLIENT_ERROR_ALL_ACCESS_DISABLED):
        logger.debug('Error from boto3: %s', exc_info=True)
        return response.status_forbidden()
    else:
        logger.exception('Error from boto3')
        return response.status_internal_error(str(e))


async def list_objects(s3: S3Client, bucket_id: str, prefix: str = None, loop: AbstractEventLoop = None) -> \
AsyncIterator[
    dict[str, Any]]:
    if not loop:
        loop_ = asyncio.get_running_loop()
    else:
        loop_ = loop
    first_time = True
    continuation_token = None
    thread_pool_executor = ThreadPoolExecutor(max_workers=10)
    while first_time or continuation_token:
        first_time = False
        list_partial = partial(s3.list_objects_v2, Bucket=bucket_id)
        if continuation_token is not None:
            list_partial = partial(list_partial, ContinuationToken=continuation_token)
        if prefix is not None:
            list_partial = partial(list_partial, Prefix=prefix)
        response_ = await loop_.run_in_executor(thread_pool_executor, list_partial)
        continuation_token = response_['NextContinuationToken'] if response_['IsTruncated'] else None
        if response_['KeyCount'] > 0:
            for obj in response_['Contents']:
                yield obj


async def is_versioning_enabled(s3: S3Client, bucket_id: str,
                                loop: asyncio.AbstractEventLoop | None = None,
                                thread_pool_executor: ThreadPoolExecutor | None = None) -> bool:
    """
    Returns true if versioning is either enabled or suspended. In other words, this function returns True if there
    may be versions to retrieve.

    :param s3: the S3 client (required).
    :param loop: optional event loop. If None or unspecified, the running loop will be used.
    :param thread_pool_executor: an optional thread pool executor.
    :return: True if versioning is enabled or suspended, False otherwise.
    """
    if not loop:
        loop_ = asyncio.get_running_loop()
    else:
        loop_ = loop
    response = await loop_.run_in_executor(thread_pool_executor, partial(s3.get_bucket_versioning, Bucket=bucket_id))
    return 'Status' in response


async def list_object_versions(s3: S3Client, bucket_id: str, prefix: str = None,
                               loop: asyncio.AbstractEventLoop | None = None) -> AsyncIterator[dict[str, Any]]:
    """
    Gets all versions of the objects with the given prefix.

    :param s3: an S3 client (required).
    :param bucket_id: the bucket id (required).
    :param prefix: the key prefix. Will get all keys in the bucket if unspecified.
    :param loop: the event loop. Will use the current running loop if unspecified.
    :return: an asynchronous iterator of dicts with the following shape:
            'ETag': 'string',
            'ChecksumAlgorithm': [
                'CRC32'|'CRC32C'|'SHA1'|'SHA256',
            ],
            'Size': 123,
            'StorageClass': 'STANDARD',
            'Key': 'string',
            'VersionId': 'string',
            'IsLatest': True|False,
            'LastModified': datetime(2015, 1, 1),
            'Owner': {
                'DisplayName': 'string',
                'ID': 'string'
            }
    """
    if not loop:
        loop_ = asyncio.get_running_loop()
    else:
        loop_ = loop
    first_time = True
    continuation_token = None
    thread_pool_executor = ThreadPoolExecutor(max_workers=10)
    while first_time or continuation_token:
        first_time = False
        list_partial = await _list_object_versions_partial(s3, bucket_id, continuation_token, prefix)
        response_ = await loop_.run_in_executor(thread_pool_executor, list_partial)
        continuation_token = response_['NextKeyMarker'] if response_['IsTruncated'] else None
        for obj in response_['Versions']:
            yield obj


async def get_object_versions_by_key(s3: S3Client, bucket_id: str, prefix: str = None,
                                     loop: asyncio.AbstractEventLoop | None = None) -> dict[str, list[dict[str, Any]]]:
    versions_by_key = {}
    async for v in list_object_versions(s3, bucket_id, prefix, loop):
        versions_by_key.setdefault(v['Key'], []).append(v)
    return versions_by_key


def to_version(v: dict[str, Any]) -> S3Version:
    version = S3Version()
    version.id = v['VersionId']
    version.modified = v['LastModified']
    version.current = v['IsLatest']
    version.set_storage_class_from_str(v['StorageClass'])
    return version


async def _list_object_versions_partial(s3: S3Client, bucket_id: str, continuation_token: str | None = None, prefix: str | None = None):
    list_partial = partial(s3.list_object_versions, Bucket=bucket_id)
    if continuation_token is not None:
        list_partial = partial(list_partial, KeyMarker=continuation_token)
    if prefix is not None:
        list_partial = partial(list_partial, Prefix=prefix)
    return list_partial


async def return_bucket_status_or_not_found(bucket_name, loop, s3):
    if loop is None:
        loop = asyncio.get_running_loop()
    try:
        await loop.run_in_executor(None, partial(s3.head_bucket, Bucket=bucket_name))
        return response.status_not_found()
    except ClientError as e:
        return handle_client_error(e)


def decode_folder(folder_id_) -> str | None:
    if folder_id_ == ROOT_FOLDER.id:
        folder_id = ''
    else:
        try:
            folder_id = decode_key(folder_id_)
            if not is_folder(folder_id):
                folder_id = None
        except KeyDecodeException:
            # Let the bucket query happen so that we consistently return Forbidden if the user lacks permissions
            # for the bucket.
            folder_id = None
    return folder_id


def key_in_folder(decoded_key, decoded_folder_key) -> bool:
    if decoded_key.startswith(decoded_folder_key):
        item_id_ = decoded_key.removeprefix(decoded_folder_key)
        if len(item_id_) > 1 and '/' in item_id_[:-1]:
            return False
    else:
        return False
    return True


async def _delete_object(s3_client: S3Client, bucket_name: str, key: str, recursive: bool) -> Response:
    loop = asyncio.get_running_loop()
    try:
        if key is None:
            return await return_bucket_status_or_not_found(bucket_name, loop, s3_client)

        response_ = await loop.run_in_executor(None, partial(s3_client.list_objects_v2, Bucket=bucket_name,
                                                             Prefix=key))
        # A key count of 0 means the folder doesn't exist. A key count of 1 just has the folder itself. A key count > 1
        # means the folder has contents.
        key_count = response_['KeyCount']
        if key_count == 0:
            return await return_bucket_status_or_not_found(bucket_name, loop, s3_client)
        if is_folder(key):
            if not recursive and key_count > 1:
                return response.status_bad_request(f'The folder {key} is not empty')
            for object_f in response_['Contents']:
                s3_client.delete_object(Bucket=bucket_name, Key=object_f['Key'])
        else:
            s3_client.delete_object(Bucket=bucket_name, Key=key)
        return await response.delete(True)
    except ClientError as e:
        return handle_client_error(e)


async def _copy_object(s3_client: S3Client, source_bucket_name, source_key_name, destination_bucket_name,
                       destination_key_name) -> web.Response:
    logger = logging.getLogger(__name__)
    try:
        s3_client.head_object(Bucket=destination_bucket_name,
                              Key=destination_key_name)  # check if destination object exists, if not throw an exception
        return response.status_bad_request(f'Object {destination_key_name} already exists')
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == '404':  # object doesn't exist
            try:
                s3_client.head_object(Bucket=source_bucket_name,
                                      Key=source_key_name)  # check if source object exists, if not throws an exception
                thread_pool_executor = ThreadPoolExecutor(max_workers=10)
                loop = asyncio.get_running_loop()

                async def _do_copy() -> AsyncIterator[asyncio.Future[None]]:
                    async for obj in list_objects(s3_client, source_bucket_name, prefix=source_key_name):
                        destination_key_ = join(destination_key_name, obj['Key'].removeprefix(source_key_name))
                        p = partial(s3_client.copy,
                                    {'Bucket': source_bucket_name, 'Key': obj['Key']},
                                    destination_bucket_name, destination_key_)
                        logger.debug('Copying %s/%s to %s/%s', source_bucket_name, obj['Key'], destination_bucket_name,
                                     destination_key_)
                        yield loop.run_in_executor(thread_pool_executor, p)

                async for coro in _do_copy():
                    await coro
                return web.HTTPCreated()
            except ClientError as e_:
                logger.exception(f'Bad request: {e_}')
                return response.status_bad_request(str(e_))
        else:
            logger.exception(f'Bad request: {e}')
            return response.status_bad_request(str(e))
