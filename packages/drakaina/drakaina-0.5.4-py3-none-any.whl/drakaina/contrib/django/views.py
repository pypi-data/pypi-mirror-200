import logging
from typing import Callable
from typing import Optional

from django.http import HttpRequest
from django.http import HttpResponse
from django.utils.module_loading import autodiscover_modules
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from drakaina.rpc_protocols import BaseRPCProtocol
from drakaina.rpc_protocols import JsonRPCv2

log = logging.getLogger(__name__)


class RPCView(View):
    """Django class based view implements JSON-RPC"""

    http_method_names = ["post", "options"]
    handler: BaseRPCProtocol
    content_type: str

    @classmethod
    def as_view(
        cls,
        autodiscover: str = "rpc_methods",
        handler: Optional[BaseRPCProtocol] = None,
        **initkwargs,
    ) -> Callable:
        """

        :param autodiscover: submodule name(s) where defined RPC methods
        :type autodiscover: str
        :param handler:
        :type handler: BaseRPCProtocol
        :param initkwargs:
        :return: Instance of this class

        """
        cls.handler = handler or JsonRPCv2()
        cls.content_type = cls.handler.content_type
        view = super().as_view(**initkwargs)
        view.cls = cls

        # Scan specified sub-modules
        autodiscover_modules(autodiscover)

        return csrf_exempt(view)

    def http_method_not_allowed(
        self,
        request: HttpRequest,
        *args,
        **kwargs,
    ) -> HttpResponse:
        msg = f"HTTP Method Not Allowed ({request.method}): {request.path}"
        content = self.handler.get_raw_error(self.handler.BadRequestError(msg))

        return HttpResponse(content=content, content_type=self.content_type)

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        if request.content_type != self.content_type or len(request.body) == 0:
            msg = f"HTTP Method Not Allowed ({request.method}): {request.path}"
            content = self.handler.get_raw_error(
                self.handler.BadRequestError(msg),
            )
        else:
            content = self.handler.handle_raw_request(
                request.body,
                request=request,
            )

        return HttpResponse(content=content, content_type=self.content_type)


# Warning! Do not commit this region
if __name__ == "__main__":
    django_view = RPCView.as_view()
