import logging
from aiohttp import ClientSession
from typing import Any, Optional
from cloudLib.const import BASE_URL
from cloudLib.exceptions import (
    CrownstoneAuthenticationError,
    CrownstoneUnknownError,
    AuthError
)

_LOGGER = logging.getLogger(__name__)


class RequestHandler:
    """Handles requests to the Crownstone lib."""

    def __init__(self) -> None:
        self.access_token: Optional[str] = None
        self.websession: Optional[ClientSession] = None
        self.login_data: Optional[dict] = None

    async def post(
            self,
            model: str,
            endpoint: str,
            model_id: str = None,
            json: dict = None
    ) -> dict:
        """
        Post request

        :param model: model type. users, spheres, stones, locations, devices.
        :param endpoint: endpoints. e.g. spheres, keys, presentPeople.
        :param model_id: required id for the endpoint. e.g. userId for users, sphereId for spheres.
        :param json: Dictionary with the data that should be posted.
        :return: Dictionary with the response from the lib.
        """
        if self.access_token is None:
            url = f'{BASE_URL}{model}/{endpoint}'
        elif model_id:
            url = f'{BASE_URL}{model}/{model_id}/{endpoint}?access_token={self.access_token}'
        else:
            url = f'{BASE_URL}{model}{endpoint}?access_token={self.access_token}'

        return await self.request('post', url, json)

    async def get(
            self,
            model: str,
            endpoint: str,
            model_id: str = None
    ) -> dict:
        """
        Get request

        :param model: model type. users, spheres, stones, locations, devices.
        :param endpoint: endpoints. e.g. spheres, keys, presentPeople.
        :param model_id: required id for the endpoint. e.g. userId for users, sphereId for spheres.
        :return: Dictionary with the response from the lib.
        """
        if model_id:
            url = f'{BASE_URL}{model}/{model_id}/{endpoint}?access_token={self.access_token}'
        else:
            url = f'{BASE_URL}{model}{endpoint}?access_token={self.access_token}'

        return await self.request('get', url)

    async def put(
            self,
            model: str,
            endpoint: str,
            model_id: str,
            command: str,
            value: Any
    ) -> dict:
        """
        Put request

        :param model: model type. users, spheres, stones, locations, devices.
        :param endpoint: endpoints. e.g. spheres, keys, presentPeople.
        :param model_id: required id for the endpoint. e.g. userId for users, sphereId for spheres.
        :param command: used for command requests. e.g. 'switchState'.
        :param value: the value to be put for the command. e.g 'switchState', 1
        :return: Dictionary with the response from the lib.
        """
        url = f'{BASE_URL}{model}/{model_id}/{endpoint}?{command}={str(value)}&access_token={self.access_token}'

        return await self.request('put', url)

    async def request(self, method: str, url: str, json: dict = None) -> dict:
        """Make request and check data for errors"""
        async with self.websession.request(method, url, json=json) as result:
            result.raise_for_status()
            data = await result.json()
            refresh = await self.raise_on_error(data)
            if refresh:
                await self.request(method, url, json=json)
            return data

    async def raise_on_error(self, data):
        """Check for error message"""
        if isinstance(data, dict) and 'error' in data:
            error = data['error']

            if 'code' in error:
                error_type = error['code']
                try:
                    AuthError(error_type)
                    if error_type == AuthError.AUTHORIZATION_REQUIRED.value:
                        await self.refresh_token()
                        return True  # re-run the request
                    else:
                        raise CrownstoneAuthenticationError(type=AuthError(error_type))
                except ValueError:
                    raise CrownstoneUnknownError("Unknown error occurred.")
            else:
                _LOGGER.error(error['message'])

            await self.websession.close()

    async def refresh_token(self):
        response = await self.post('users', 'login', json=self.login_data)
        self.access_token = response['id']
