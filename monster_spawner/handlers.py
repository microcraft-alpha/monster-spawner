"""App exception handlers."""

from fastapi import Request, responses
from starlette import status

from monster_spawner.domain import exceptions


async def does_not_exist_handler(
    request: Request,
    exc: exceptions.DoesNotExistError,
) -> responses.JSONResponse:
    """Handle DoesNotExistError.

    Args:
        request (Request): request object.
        exc (DoesNotExistError): exception object.

    Returns:
        JSONResponse: json response.
    """
    return responses.JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": f"{exc.entry_name} does not exist - {exc.id}"},
    )


async def already_exists_handler(
    request: Request,
    exc: exceptions.AlreadyExistsError,
) -> responses.JSONResponse:
    """Handle AlreadyExistsError.

    Args:
        request (Request): request object.
        exc (AlreadyExistsError): exception object.

    Returns:
        JSONResponse: json response.
    """
    return responses.JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": f"{exc.entry_name} already exists - {exc.id}"},
    )


EXCEPTION_HANDLERS = frozenset(
    {
        exceptions.DoesNotExistError: does_not_exist_handler,
        exceptions.AlreadyExistsError: already_exists_handler,
    }.items(),
)
