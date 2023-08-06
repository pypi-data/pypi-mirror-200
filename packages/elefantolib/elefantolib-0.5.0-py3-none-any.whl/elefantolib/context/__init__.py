from elefantolib.context import context_service
from elefantolib import provider

from http_client import httpx_client


class BaseContext:
    HTTP_CLIENT = None
    CONTEXT_ATTRIBUTES = (
        'auth_token',
        'correlation_id',
        'locale',
    )

    def __init__(self, pvr: provider.Provider):
        for attribute in self.CONTEXT_ATTRIBUTES:
            setattr(self, attribute, getattr(pvr, attribute, None))

        self.services = context_service.ContextService(self.HTTP_CLIENT, self.context)

    @property
    def context(self):
        return {a: getattr(self, a) for a in self.CONTEXT_ATTRIBUTES}


class PlatformContext(BaseContext):
    HTTP_CLIENT = httpx_client.HttpxClient


class AsyncPlatformContext(BaseContext):
    HTTP_CLIENT = httpx_client.AsyncHttpxClient
