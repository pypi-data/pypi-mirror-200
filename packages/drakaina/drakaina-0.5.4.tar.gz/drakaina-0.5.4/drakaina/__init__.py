from asyncio import iscoroutinefunction
from functools import update_wrapper
from typing import Any
from typing import Callable
from typing import Optional
from typing import TypeVar

from drakaina.registries import RPCRegistry

__all__ = (
    "RPCRegistry",
    "rpc_registry",
    "remote_procedure",
    "ENV_APP",
    "ENV_IS_AUTHENTICATED",
    "ENV_USER",
    "ENV_USER_ID",
    "ENV_JWT_PAYLOAD",
    "ENV_JWT_SCOPES",
)

# General registry
rpc_registry = RPCRegistry()

T = TypeVar("T")

# Environ (Request) context
ENV_APP = "drakaina.app"
ENV_IS_AUTHENTICATED = "drakaina.is_authenticated"
ENV_USER = "user"
ENV_USER_ID = "user_id"
ENV_JWT_PAYLOAD = "drakaina.jwt.payload"
ENV_JWT_SCOPES = "drakaina.jwt.scopes"


def remote_procedure(
    name: Optional[str] = None,
    registry: Optional[RPCRegistry] = None,
    provide_request: Optional[bool] = None,
    metadata: Optional[dict[str, Any]] = None,
    **meta_options,
) -> Callable:
    """Decorator allow wrap function and define it as remote procedure.

    :param name:
        Procedure name. Default as function name.
    :type name: str
    :param registry:
        Procedure registry custom object
    :type registry: RPCRegistry
    :param provide_request:
        Provide a request object or context data (from the transport layer).
        If `True`, then the request object or context can be supplied to
        the procedure as a `request` argument.
    :type provide_request: bool
    :param metadata:
        Metadata that can be processed by middleware.
    :type metadata: dict[str, Any]
    :param meta_options:
        Metadata that can be processed by middleware.

    """

    if callable(name):
        return __decorator(
            name,
            registry,
            None,
            provide_request,
            metadata=metadata,
            **meta_options,
        )
    elif not isinstance(name, (str, type(None))):
        raise TypeError(
            "Expected first argument to be an str, a callable, or None",
        )

    def decorator(procedure):
        assert callable(procedure)
        return __decorator(
            procedure,
            registry,
            name,
            provide_request,
            metadata=metadata,
            **meta_options,
        )

    return decorator


def __decorator(
    procedure: T,
    registry: RPCRegistry = None,
    name: str = None,
    provide_request: bool = None,
    **meta_options,
) -> T:
    """Returns a registered procedure"""

    if iscoroutinefunction(procedure):

        async def wrapper(*args, **kwargs):
            if not provide_request:
                if len(args) == 0:
                    kwargs.pop("request")
                else:
                    scope, *args = args
            return await procedure(*args, **kwargs)

    else:

        def wrapper(*args, **kwargs):
            if not provide_request:
                if len(args) == 0:
                    kwargs.pop("request")
                else:
                    environ, *args = args
            return procedure(*args, **kwargs)

    # Need to update the wrapper before registering in the registry
    decorated_procedure = update_wrapper(wrapper, procedure)

    _registry = registry if registry is not None else rpc_registry
    name = procedure.__name__ if name is None else name
    metadata = meta_options.pop("metadata") or {}
    _registry.register_procedure(
        decorated_procedure,
        name=name,
        provide_request=provide_request,
        metadata={**metadata, **meta_options},
    )

    return decorated_procedure
