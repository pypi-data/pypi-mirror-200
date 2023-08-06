import logging
from functools import partial

import httpx

from elefantolib.http_client import BaseClient


logger = logging.getLogger(__name__)


class HttpxClient(BaseClient):

    def __getattr__(self, item):
        return partial(self._request, method=item)

    def _request(self, method: str, path: str, raises: bool = False, **kwargs):
        with httpx.Client(headers=self.headers) as client:
            kwargs['headers'] = {**self.headers, **kwargs.get('headers', {})}

            try:
                resp = getattr(client, method)(f'{self.api_url}/{path}', **kwargs)

                return (resp, None) if not raises else resp
            except Exception as e:
                logger.error(e)
                return (None, e) if not raises else None


class AsyncHttpxClient(BaseClient):

    def __getattr__(self, item):
        return partial(self._request, method=item)

    async def _request(self, method: str, path: str, raises: bool = False, **kwargs):
        async with httpx.AsyncClient(headers=self.headers) as client:
            kwargs['headers'] = {**self.headers, **kwargs.get('headers', {})}

            try:
                resp = await getattr(client, method)(f'{self.api_url}/{path}', **kwargs)

                return (resp, None) if not raises else resp
            except BaseException as e:
                logger.error(e)
                return (None, e) if not raises else None
