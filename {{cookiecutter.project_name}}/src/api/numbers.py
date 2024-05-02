from fastapi import APIRouter, Depends
from src.use_cases.numbers.divide import get_divide_case, DivideResponse
from src.use_cases.numbers.multiply import get_multiply_use_case, MultiplyResponse
from src.use_cases.numbers.subtract import get_subtract_use_case, SubtractResponse
from src.use_cases.numbers.summarise import get_summarise_use_case, SummariseResponse

routes = APIRouter(tags=['numbers'])


@routes.post('/numbers', response_model=SummariseResponse)
async def summarise_numbers(
        numbers: SummariseRequest,
        use_case: SummariseUseCase = Depends(get_summarise_use_case)
) -> SummariseResponse:
    result: SummariseResponse = await use_case.execute(numbers)
    return result


@routes.get('/numbers', response_model=SubtractResponse)
async def subtract_numbers(
        num_left: int,
        num_right: int,
        use_case: SubtractUseCase = Depends(get_subtract_use_case)
) -> SubtractResponse:
    request_object: SubtractRequest = SubtractRequest(left=num_left, right=num_right)
    result: SubtractResponse = await use_case.execute(request_object)
    return result


@routes.put('/numbers', response_model=MultiplyResponse)
async def multiply_numbers(
        numbers: MultiplyRequest,
        use_case: MultiplyUseCase = Depends(get_multiply_use_case)
) -> MultiplyResponse:
    result: MultiplyResponse = await use_case.execute(numbers)
    return result


@routes.delete('/numbers', response_model=DivideResponse)
async def divide_numbers(
        num_left: int,
        num_right: int,
        use_case: DivideUseCase = Depends(get_divide_case)
) -> DivideResponse:
    request_object: DivideRequest = DivideRequest(left=num_left, right=num_right)
    result: DivideResponse = await use_case.execute(request_object)
    return result
