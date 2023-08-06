from drakaina.middlewares.base import BaseMiddleware
from drakaina.typing_ import ASGIReceive
from drakaina.typing_ import ASGIScope
from drakaina.typing_ import ASGISend
from drakaina.typing_ import ProxyRequest
from drakaina.typing_ import WSGIEnvironment
from drakaina.typing_ import WSGIResponse
from drakaina.typing_ import WSGIStartResponse


class RequestWrapperMiddleware(BaseMiddleware):
    """The middleware for wrapping the request object.

    Provides access to the mapping environment object through
    the attribute access interface. This is needed for some
    backward compatibility in cases where the request is
    an object with attributes, such as `request.user`.

    """

    def __wsgi_call__(
        self,
        environ: WSGIEnvironment,
        start_response: WSGIStartResponse,
    ) -> WSGIResponse:
        return self.app(ProxyRequest(environ), start_response)

    async def __asgi_call__(
        self,
        scope: ASGIScope,
        receive: ASGIReceive,
        send: ASGISend,
    ):
        await self.app(ProxyRequest(scope), receive, send)
