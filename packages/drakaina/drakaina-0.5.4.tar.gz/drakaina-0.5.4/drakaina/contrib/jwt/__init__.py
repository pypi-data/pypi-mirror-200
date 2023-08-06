"""Submodule with implementations support of JSON Web Tokens

Standard: https://www.rfc-editor.org/rfc/rfc7519
"""
from __future__ import annotations

from asyncio import iscoroutinefunction
from functools import update_wrapper
from typing import Callable
from typing import Iterable
from typing import Optional
from typing import TypeVar

from drakaina import ENV_IS_AUTHENTICATED
from drakaina import ENV_JWT_SCOPES
from drakaina._types import ASGIScope
from drakaina._types import WSGIEnvironment
from drakaina.contrib.jwt.errors import InvalidJWTTokenError
from drakaina.contrib.jwt.types import Comparator
from drakaina.exceptions import ForbiddenError
from drakaina.registries import is_rpc_procedure
from drakaina.utils import iterable_str_arg

__all__ = (
    "check_permissions",
    "login_required",
    "match_all",
    "match_any",
    "RESERVED_FIELDS",
    "SUPPORTED_ALGORITHMS",
)

RESERVED_FIELDS = ("iss", "sub", "aud", "exp", "nbf", "iat", "jti")
SUPPORTED_ALGORITHMS = ("HS256", "HS384", "HS512", "RS256", "RS384", "RS512")

T = TypeVar("T")


def login_required(*_args) -> Callable:
    """Requires login decorator.

    Gives access to the procedure only to authenticated users.

    """

    def __decorator(procedure: T) -> T:
        """Returns a registered procedure"""
        if not is_rpc_procedure(procedure):
            raise TypeError(
                "Incorrect usage of decorator. Please use "
                "the `drakaina.remote_procedure` decorator first.",
            )

        if iscoroutinefunction(procedure):

            async def wrapper(*args, **kwargs):
                if len(args) == 0:
                    scope: ASGIScope = kwargs.get("request")
                else:
                    scope: ASGIScope = args[0]

                if not scope.get(ENV_IS_AUTHENTICATED, False):
                    raise ForbiddenError("Authorization required")
                return await procedure(*args, **kwargs)

        else:

            def wrapper(*args, **kwargs):
                if len(args) == 0:
                    environ: WSGIEnvironment = kwargs.get("request")
                else:
                    environ: WSGIEnvironment = args[0]

                if not environ.get(ENV_IS_AUTHENTICATED, False):
                    raise ForbiddenError("Authorization required")
                return procedure(*args, **kwargs)

        return update_wrapper(wrapper, procedure)

    if len(_args) > 0:
        if callable(_args[0]):
            return __decorator(_args[0])
        else:
            raise TypeError("Expected first argument to be a callable")

    def decorator(procedure):
        assert callable(procedure)
        return __decorator(procedure)

    return decorator


def match_any(
    required: Iterable[str],
    provided: str | Iterable[str],
) -> bool:
    return any((scope in provided for scope in required))


def match_all(
    required: Iterable[str],
    provided: str | Iterable[str],
) -> bool:
    return set(required).issubset(set(provided))


def check_permissions(
    scopes: str | Iterable[str],
    comparator: Comparator = match_all,
) -> Callable:
    """Permission decorator.

    Gives access to the procedure only to authorized users.

    """
    if not callable(comparator):
        raise TypeError("comparator should be a func")

    procedure_scopes = iterable_str_arg(scopes)

    def decorator(procedure: T) -> T:
        if not is_rpc_procedure(procedure):
            raise TypeError(
                "Incorrect usage of decorator. Please use "
                "the `drakaina.remote_procedure` decorator first.",
            )

        if iscoroutinefunction(procedure):

            async def wrapper(*args, **kwargs):
                if len(args) == 0:  # noqa
                    scope: ASGIScope = kwargs.get("request")
                else:
                    scope: ASGIScope = args[0]

                if not scope.get(ENV_IS_AUTHENTICATED, False):
                    raise ForbiddenError("Authorization required")

                user_scopes = _get_scopes(scope)
                if not isinstance(user_scopes, Iterable):
                    raise InvalidJWTTokenError("Invalid permissions format")

                if not comparator(procedure_scopes, user_scopes):
                    raise ForbiddenError("Forbidden")

                return await procedure(*args, **kwargs)

        else:

            def wrapper(*args, **kwargs):
                if len(args) == 0:  # noqa
                    environ: WSGIEnvironment = kwargs.get("request")
                else:
                    environ: WSGIEnvironment = args[0]

                if not environ.get(ENV_IS_AUTHENTICATED, False):
                    raise ForbiddenError("Authorization required")

                user_scopes = _get_scopes(environ)
                if not isinstance(user_scopes, Iterable):
                    raise InvalidJWTTokenError("Invalid permissions format")

                if not comparator(procedure_scopes, user_scopes):
                    raise ForbiddenError("Forbidden")

                return procedure(*args, **kwargs)

        return update_wrapper(wrapper, procedure)

    return decorator


def _get_scopes(
    request: WSGIEnvironment | ASGIScope,
) -> Optional[Iterable[str]]:
    scopes = request.get(ENV_JWT_SCOPES)
    if scopes:
        return iterable_str_arg(scopes)
