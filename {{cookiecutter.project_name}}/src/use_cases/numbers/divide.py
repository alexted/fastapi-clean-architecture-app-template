import logging

from pydantic import BaseModel

from src.use_cases.base import BaseUseCase

logger = logging.getLogger()


class DivideRequest(BaseModel):
    x: int
    y: int


class DivideResponse(BaseModel):
    sum: int


class DivideUseCase(BaseUseCase):

    async def execute(self, request_object: DivideRequest) -> DivideResponse:
        logger.info('test message')
        return DivideResponse(sum=request_object.x + request_object.y)


async def get_divide_case():
    return DivideUseCase()
