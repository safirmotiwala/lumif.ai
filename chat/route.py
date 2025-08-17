from fastapi import APIRouter

from chat.service import chat_service, stream_chat_service
from utilities.utils import sse_response_example

router = APIRouter(
    prefix="/chat_service",
    tags=["Chat"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)

router.post("/invoke/", responses={403: {"description": "Operation forbidden"}})(chat_service)
router.post("/ainvoke/", responses=sse_response_example())(stream_chat_service)