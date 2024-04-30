import logging

from pydantic import BaseModel

from src.app.config import config
from src.use_cases.base import BaseUseCase

logger = logging.getLogger(config.APP_NAME)


class SumRequest(BaseModel):
    x: int
    y: int


class SumResponse(BaseModel):
    sum: int


class Sum(BaseUseCase):

    async def execute(self, request_object: SumRequest) -> SumResponse:
        logger.info('test message')
        return SumResponse(sum=request_object.x + request_object.y)


async def get_sum_use_case():
    return Sum()
