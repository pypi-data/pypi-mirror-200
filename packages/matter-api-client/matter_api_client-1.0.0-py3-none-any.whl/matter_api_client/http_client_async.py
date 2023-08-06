import logging
import orjson
from aiohttp import ClientSession, ClientError

from .decorators import retry_if_failed
from .response import Response
from .exceptions import APIClientError


async def _process_response(response) -> Response:
    text = await response.text()

    try:
        json = orjson.loads(text)
    except orjson.JSONDecodeError:
        return Response(status_code=response.status, text=text)
    else:
        return Response(status_code=response.status, text=text, json=json)


@retry_if_failed
async def get(url: str, headers: {} = None) -> Response:
    async with ClientSession() as session:
        try:
            async with session.get(url=url, headers=headers) as response:
                return await _process_response(response)
        except ClientError as ex:
            logging.error(f"API Client Error: {str(ex)}")
            raise APIClientError(
                description=str(ex),
                detail=ex,
            )


@retry_if_failed
async def post(url: str, payload: dict = None, headers: dict = None) -> Response:
    async with ClientSession() as session:
        try:
            async with session.post(url=url, json=payload, headers=headers) as response:
                return await _process_response(response)
        except ClientError as ex:
            logging.error(f"API Client Error: {str(ex)}")
            raise APIClientError(
                description=str(ex),
                detail=ex,
            )


@retry_if_failed
async def put(url: str, payload: dict = None, headers: dict = None) -> Response:
    async with ClientSession() as session:
        try:
            async with session.put(url=url, json=payload, headers=headers) as response:
                return await _process_response(response)
        except ClientError as ex:
            logging.error(f"API Client Error: {str(ex)}")
            raise APIClientError(
                description=str(ex),
                detail=ex,
            )


@retry_if_failed
async def delete(url: str, payload: dict = None, headers: dict = None) -> Response:
    async with ClientSession() as session:
        try:
            async with session.delete(url=url, json=payload, headers=headers) as response:
                return await _process_response(response)
        except ClientError as ex:
            logging.error(f"API Client Error: {str(ex)}")
            raise APIClientError(
                description=str(ex),
                detail=ex,
            )
