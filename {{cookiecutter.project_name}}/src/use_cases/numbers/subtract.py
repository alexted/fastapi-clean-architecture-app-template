import logging

from pydantic import BaseModel

from src.use_cases.base import BaseUseCase

logger = logging.getLogger()


class SubtractRequest(BaseModel):
    x: int
    y: int


class SubtractResponse(BaseModel):
    sum: int


class SubtractUseCase(BaseUseCase):

    async def execute(self, request_object: SubtractRequest) -> SubtractResponse:
        logger.info('test message')
        return SubtractResponse(sum=request_object.x + request_object.y)
