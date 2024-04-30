import uuid

from starlette.requests import Request

from .request_id_manager import request_id_manager


async def handle_request_id(request: Request, call_next):
    request_id = request.headers.get('X-Request-ID') or str(uuid.uuid4())
    request_id_manager.set(request_id)
    response = await call_next(request)
    response.headers['X-Request-ID'] = request_id
    request_id_manager.reset()
    return response
