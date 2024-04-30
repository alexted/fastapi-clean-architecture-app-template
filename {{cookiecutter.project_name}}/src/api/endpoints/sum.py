from fastapi import APIRouter, Depends

from src.use_cases.sum import get_sum_use_case, SumResponse, Sum, SumRequest

routes = APIRouter()


@routes.post('/sum', response_model=SumResponse, tags=['sum'])
async def sum_numbers(item: SumRequest, use_case: Sum = Depends(get_sum_use_case)) -> SumResponse:
    item: SumResponse = await use_case.execute(item)
    return item
