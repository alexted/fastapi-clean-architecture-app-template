from __future__ import annotations

from typing import Annotated

from fastapi import Query, Depends, APIRouter

from src.domain.use_cases.numbers import (
    DivideRequest,
    DivideUseCase,
    DivideResponse,
    MultiplyRequest,
    MultiplyUseCase,
    SubtractRequest,
    SubtractUseCase,
    MultiplyResponse,
    SubtractResponse,
    SummariseRequest,
    SummariseUseCase,
    SummariseResponse,
)

routes = APIRouter(tags=["numbers"])


@routes.post("/summarise")
async def summarise_numbers(
    numbers: SummariseRequest, use_case: Annotated[SummariseUseCase, Depends(SummariseUseCase)]
) -> SummariseResponse:
    result: SummariseResponse = await use_case.execute(numbers)
    return result


@routes.get("/subtract")
async def subtract_numbers(
    minuend: Annotated[int, Query(title="minuend", examples=[45678, 67890, 90123])],
    subtrahend: Annotated[int, Query(title="subtrahend", examples=[12345, 45678, 78901])],
    use_case: Annotated[SubtractUseCase, Depends(SubtractUseCase)],
) -> SubtractResponse:
    request_object: SubtractRequest = SubtractRequest(left_number=minuend, right_number=subtrahend)
    result: SubtractResponse = await use_case.execute(request_object)
    return result


@routes.put("/multiply")
async def multiply_numbers(
    numbers: MultiplyRequest, use_case: Annotated[MultiplyUseCase, Depends(MultiplyUseCase)]
) -> MultiplyResponse:
    result: MultiplyResponse = await use_case.execute(numbers)
    return result


@routes.delete("/divide")
async def divide_numbers(
    dividend: Annotated[int, Query(title="dividend", examples=[12345, 45678, 78901])],
    divisor: Annotated[int, Query(title="divisor", examples=[12, 45, 901])],
    use_case: Annotated[DivideUseCase, Depends(DivideUseCase)],
) -> DivideResponse:
    request_object: DivideRequest = DivideRequest(dividend=dividend, divisor=divisor)
    result: DivideResponse = await use_case.execute(request_object)
    return result
