from uuid import UUID
from typing import Annotated
import logging

from fastapi import Depends, Request, HTTPException
from pydantic import BaseModel

from src.constants import ProjectRole, OrganisationRole
from src.data.authn.idp import IDPService
from src.service.config import AppConfig, get_config
from src.data.employees.repository import EmployeeDTO, EmployeeFilters, EmployeeRepository

logger = logging.getLogger()


class Userinfo(BaseModel):
    sub: UUID


class User(BaseModel):
    id: UUID
    org_role: ProjectRole
    project_role: OrganisationRole


async def get_idp_client(config: Annotated[AppConfig, Depends(get_config)]) -> IDPService:
    return IDPService.new(config)


async def get_user_info(request: Request, idp_client: Annotated[IDPService, Depends(get_idp_client)]) -> Userinfo:
    token = request.headers.get("Authorization", "")
    token_parts = token.split("Bearer ")
    if len(token_parts) != 2:
        raise HTTPException(status_code=401, detail="Invalid token")

    try:
        user_info = await idp_client.get_user_info(token_parts[1])
        return Userinfo.model_validate(user_info) if user_info is not None else None
    except Exception as e:
        logger.error(f"Error getting userinfo: {type(e)}")
        raise HTTPException(status_code=401, detail="Cannot get userinfo") from e


async def get_current_employee(
    user_info: Annotated[Userinfo, Depends(get_user_info)],
    employee_repo: Annotated[EmployeeRepository, Depends(EmployeeRepository)],
) -> User:
    employee: EmployeeDTO | None = await employee_repo.get(EmployeeFilters(ids=[user_info.sub]))
    if not employee:
        raise HTTPException(status_code=401, detail="User not found")

    # TODO - Implement role mapping when employee roles will be implemented
    return User(id=employee.id, role=ProjectRole.ADMIN)


def require_role(roles: list[ProjectRole]) -> callable:
    def dependency(current_user: EmployeeDTO = Depends(get_current_employee)) -> None:
        if current_user.role not in roles:
            raise HTTPException(status_code=403, detail="Forbidden")

    return dependency


# TODO - Implement project id validation
