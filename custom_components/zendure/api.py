"""Sample API Client."""
from __future__ import annotations

import socket

import aiohttp
import async_timeout
import const


class ZendureApiClientError(Exception):
    """Exception to indicate a general API error."""
    const.LOGGER.error("API-Error!")


class ZendureApiClientCommunicationError(
    ZendureApiClientError
):
    """Exception to indicate a communication error."""


class ZendureApiClientAuthenticationError(
    ZendureApiClientError
):
    """Exception to indicate an authentication error."""


class ZendureApiClient:
    """Zendure API Client."""

    def __init__(
            self,
            username: str,
            password: str,
            language: str,
            session: aiohttp.ClientSession,
    ) -> None:
        """Sample API Client."""
        self._username = username
        self._password = password
        self._session = session
        self._language = language
        self._authtoken = "(null)"

    async def async_get_data(self) -> any:
        """Get data from the API."""
        return await self._api_wrapper(
            method="get", url="https://jsonplaceholder.typicode.com/posts/1"
        )

    async def async_set_title(self, value: str) -> any:
        """Get data from the API."""
        return await self._api_wrapper(
            method="patch",
            url="https://app.zendure.tech/v2",
            data={"title": value},
            headers={'Content-Type': 'application/json',
                     'Accept-Language': self._language,
                     'appVersion': '5.0.0',
                     'User-Agent': 'Zendure/5.0.0 (iPhone; iOS 17.6.1; Scale/3.00)',
                     'Accept': '*/*',
                     'Authorization': 'Basic Q29uc3VtZXJBcHA6NX4qUmRuTnJATWg0WjEyMw==',
                     'Blade-Auth': f'bearer {self._authtoken}'},
        )

    async def async_get_token(self):
        """Get the Auth-Token for future Requests"""
        apiTokenJson = await self._api_wrapper(
            method="post",
            url=f'{const.ZEN_API_URL}{const.ZEN_AUTH_PATH}',
            data={
                'password': self._password,
                'account': self._username,
                'appId': '121c83f761305d6cf7e',
                'appType': 'iOS',
                'grantType': 'password',
                'tenantId': ''
            }
        )
        if len(apiTokenJson.data.accessToken) == 0:
            const.LOGGER.error("No Token received")
        else:
            self._authtoken = apiTokenJson.data.accessToken

    async def async_get_devices(self) -> dict:
        api = await self._api_wrapper(
            method="post",
            url=f'{const.ZEN_API_URL}{const.ZEN_DEVICELIST_PATH}',
        )

    async def _api_wrapper(
            self,
            method: str,
            url: str,
            data: dict | None = None,
            headers: dict | None = None,
    ) -> any:
        """Get information from the API."""
        try:
            async with async_timeout.timeout(10):
                response = await self._session.request(
                    method=method,
                    url=url,
                    headers=headers,
                    json=data,
                )
                if response.status in (401, 403):
                    raise ZendureApiClientAuthenticationError(
                        "Invalid credentials",
                    )
                response.raise_for_status()
                return await response.json()

        except TimeoutError as exception:
            raise ZendureApiClientCommunicationError(
                "Timeout error fetching information",
            ) from exception
        except (aiohttp.ClientError, socket.gaierror) as exception:
            raise ZendureApiClientCommunicationError(
                "Error fetching information",
            ) from exception
        except Exception as exception:  # pylint: disable=broad-except
            raise ZendureApiClientError(
                "Something really wrong happened!"
            ) from exception
