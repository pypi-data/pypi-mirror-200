from heaserver.service.runner import routes
from heaserver.service.db import awsservicelib
from heaserver.service import response
from heaserver.service.appproperty import HEA_DB
from aiohttp import web
import logging

_logger = logging.getLogger(__name__)


@routes.get('/accounts/{id}')
async def get_volume_id(request: web.Request) -> web.Response:
    volume_id = await awsservicelib.get_volume_id_for_account_id(request)
    if volume_id is not None:
        return response.status_ok(body=volume_id)
    else:
        return response.status_not_found()


@routes.get('/properties/{id}')
async def get_properties_id(request: web.Request) -> web.Response:
    property = await request.app[HEA_DB].get_property(request.app, request.match_info['id'])
    if property is not None:
        return response.status_ok(body=property.to_json())
    else:
        return response.status_not_found()
