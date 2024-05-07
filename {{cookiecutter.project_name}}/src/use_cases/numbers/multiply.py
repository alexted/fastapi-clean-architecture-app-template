import logging

from pydantic import BaseModel

from src.use_cases.base import BaseUseCase

logger = logging.getLogger()


class MultiplyRequest(BaseModel):
    x: int
    y: int


class MultiplyResponse(BaseModel):
    sum: int


class MultiplyUseCase(BaseUseCase):

    async def execute(self, request_object: MultiplyRequest) -> MultiplyResponse:
        logger.info('test message')
        return MultiplyResponse(sum=request_object.x + request_object.y)


async def get_multiply_use_case():
    return MultiplyUseCase()
