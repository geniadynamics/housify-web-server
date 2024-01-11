from asyncio import timeout
from fastapi import APIRouter, Depends, HTTPException
from data.models.user import User
from fastapi.security import HTTPBearer
from fastapi import APIRouter, Depends, HTTPException, Depends
from data.models.user import User
from async_fastapi_jwt_auth import AuthJWT
from data.schemas.request import RequestSchemaIn, RequestSchemaOut
from data.models.request import Request
from pydantic import UUID4
from typing import List
from uuid import uuid4
import httpx

router = APIRouter()
ui_auth_rule = HTTPBearer()


@router.post("/inference-request", response_model=RequestSchemaOut)
async def process_inference_request(data: RequestSchemaIn):
    user = await User.get(email=data.user)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    async with httpx.AsyncClient(timeout=120) as client:
        response = await client.post(
            "http://192.168.1.21:8082/inference-request", json=data.model_dump()
        )
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code, detail="External service error"
            )

        external_data = response.json()

        response = RequestSchemaOut(**external_data)
        await create_request(response, user.id)
        return response


async def create_request(data: RequestSchemaOut, user_uuid: UUID4):
    user = await User.get_or_none(id=user_uuid)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    new_request = await Request.create(
        id=uuid4().hex,
        user=user,
        input=data.input,
        r_type="",
        img_input=data.img_input,
        img_output=data.img_output,
        output_description=data.output_description,
        output_classification=data.output_classification,
        request_classification=data.request_classification,
        is_public=data.is_public,
        finished_state="",
    )

    return new_request


@router.get("/user-requests", response_model=List[RequestSchemaOut])
async def get_user_requests(email: str):
    user = await User.get_or_none(email=email)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    requests = await Request.filter(user=user).all()

    return [RequestSchemaOut.from_orm(request) for request in requests]
