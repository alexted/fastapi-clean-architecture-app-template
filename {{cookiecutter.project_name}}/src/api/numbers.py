from typing import Annotated

from fastapi import APIRouter, Depends
from src.use_cases.numbers import (
    DivideRequest,
    DivideResponse,
    DivideUseCase,
    MultiplyRequest,
    MultiplyResponse,
    MultiplyUseCase,
    SubtractRequest,
    SubtractResponse,
    SubtractUseCase,
    SummariseRequest,
    SummariseResponse,
    SummariseUseCase
)

routes = APIRouter(tags=['numbers'])


@routes.post('/numbers', response_model=SummariseResponse)
async def summarise_numbers(
        numbers: SummariseRequest,
        use_case: Annotated[SummariseUseCase, Depends(SummariseUseCase)]
) -> SummariseResponse:
    result: SummariseResponse = await use_case.execute(numbers)
    return result


@routes.get('/numbers', response_model=SubtractResponse)
async def subtract_numbers(
        num_left: Annotated[int, Query()],
        num_right: Annotated[int, Query()],
        use_case: Annotated[SubtractUseCase, Depends(SubtractUseCase)]
) -> SubtractResponse:
    request_object: SubtractRequest = SubtractRequest(left=num_left, right=num_right)
    result: SubtractResponse = await use_case.execute(request_object)
    return result


@routes.put('/numbers', response_model=MultiplyResponse)
async def multiply_numbers(
        numbers: MultiplyRequest,
        use_case: Annotated[MultiplyUseCase, Depends(MultiplyUseCase)]
) -> MultiplyResponse:
    result: MultiplyResponse = await use_case.execute(numbers)
    return result


@routes.delete('/numbers', response_model=DivideResponse)
async def divide_numbers(
        num_left: int,
        num_right: int,
        use_case: Annotated[DivideUseCase, Depends(DivideUseCase)]
) -> DivideResponse:
    request_object: DivideRequest = DivideRequest(left=num_left, right=num_right)
    result: DivideResponse = await use_case.execute(request_object)
    return result
