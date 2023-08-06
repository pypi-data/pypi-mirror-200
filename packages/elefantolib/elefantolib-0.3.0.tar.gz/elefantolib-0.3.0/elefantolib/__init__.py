from .context import BaseContext, PlatformContext, AsyncPlatformContext
from .context.context_service import ContextService

from .provider import Provider, DictProvider
from .provider.django_provider import DjangoProvider

from .http_client import BaseClient
from .http_client.httpx_client import HttpxClient, AsyncHttpxClient

from .constants import SERVICE_MAIN_URL

from .middleware import DjangoPlatformContextMiddleware, DjangoAsyncPlatformContextMiddleware


__version__ = '0.3.0'


__all__ = (
    '__version__',
    'BaseContext',
    'PlatformContext',
    'AsyncPlatformContext',
    'ContextService',
    'Provider',
    'DictProvider',
    'DjangoProvider',
    'BaseClient',
    'HttpxClient',
    'AsyncHttpxClient',
    'SERVICE_MAIN_URL',
    'DjangoPlatformContextMiddleware',
    'DjangoAsyncPlatformContextMiddleware',

)

__locals = locals()
for __name in __all__:
    if not __name.startswith("__"):
        setattr(__locals[__name], "__module__", "elefantolib")  # noqa
