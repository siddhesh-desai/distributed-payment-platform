"""GET /sample/hello — scaffold demonstrator endpoint."""

from fastapi import APIRouter

from modules.sample_module.public.facades import HelloFacade
from modules.sample_module.routes.responses import HelloResponse

router = APIRouter()


@router.get("/hello", response_model=HelloResponse)
def get_hello() -> HelloResponse:
    return HelloResponse(
        message=HelloFacade.say_hello(),
        module="sample_module",
    )
