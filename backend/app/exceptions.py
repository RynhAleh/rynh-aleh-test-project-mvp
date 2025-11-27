from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError


async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    errors = {}
    for err in exc.errors():
        field = err["loc"][-1]
        msg = err["msg"]

        if msg.lower().startswith("value error"):
            if "," in msg:
                msg = msg.split(",", 1)[1].strip()

        errors.setdefault(field, []).append(msg)

    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"success": False, "error": errors}
    )
