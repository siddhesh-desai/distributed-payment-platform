"""GET /sample/hello — scaffold demonstrator endpoint."""

from fastapi import APIRouter

from modules.sample_module.routes.outputs.hello_output import HelloResponse
from modules.sample_module.services.hello_service import HelloService

router = APIRouter()


@router.get("/hello", response_model=HelloResponse)
def get_hello() -> HelloResponse:
    service_msg = HelloService.say_hello()
    return HelloResponse(message=service_msg, module="sample_module")
