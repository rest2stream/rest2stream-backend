from typing import Optional, List
from fastapi import APIRouter, Depends
from pydantic import BaseModel, HttpUrl
from tortoise.contrib.fastapi import HTTPNotFoundError
from models import MyApiPydantic, MyApisInPydantic, MyApis
from .accounts import get_current_user 

router = APIRouter()


class Status(BaseModel):
    message: str


@router.get("/list", response_model=List[MyApiPydantic])
async def list_myapi(token: str = Depends(get_current_user)):
    return await MyApiPydantic.from_queryset(MyApis.filter(created_by_id=token.id))

@router.post("/create", response_model=MyApiPydantic)
async def create_myapi(myapi: MyApisInPydantic, _ = Depends(get_current_user)):
    myapi_obj = await MyApis.create(**myapi.dict(exclude_unset=True))
    return await MyApiPydantic.from_tortoise_orm(myapi_obj)

@router.get(
    "/{myapi_id}", response_model=MyApiPydantic, responses={404: {"model": HTTPNotFoundError}}
)
async def get_myapi(myapi_id: int, _ = Depends(get_current_user)):
    return await MyApiPydantic.from_queryset_single(MyApis.get(id=myapi_id))

@router.put(
    "/{myapi_id}", response_model=MyApiPydantic, responses={404: {"model": HTTPNotFoundError}}
)
async def update_myapi(myapi_id: int, myapi: MyApisInPydantic, _ = Depends(get_current_user)):
    await MyApis.filter(id=myapi_id).update(**myapi.dict(exclude_unset=True))
    return await MyApiPydantic.from_queryset_single(MyApis.get(id=myapi_id))

@router.delete("/{myapi_id}", response_model=Status, responses={404: {"model": HTTPNotFoundError}})
async def delete_myapi(myapi_id: int, _ = Depends(get_current_user)):
    deleted_count = await MyApis.filter(id=myapi_id).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail=f"MyApi {myapi_id} not found")
    return Status(message=f"Deleted myapi {myapi_id}")
