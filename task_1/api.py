from fastapi import APIRouter, Depends, HTTPException, status
from redis.asyncio import Redis

from deps import get_redis_instance
from schemas import DataSchema

router = APIRouter()


@router.get("/check_data/{phone}", response_model=DataSchema)
async def check_data(phone: str, redis: Redis = Depends(get_redis_instance)) -> DataSchema:
    """
    Get data by phone number.
    If record does not exist returns 404 status code
    """
    if not phone.isdigit():
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Phone must be digit")

    address = await redis.get(name=phone)

    if not address:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Record not found")

    return DataSchema(phone=phone, address=address)


@router.post("/write_data", response_model=DataSchema, status_code=status.HTTP_201_CREATED)
async def add_data(request_data: DataSchema, redis: Redis = Depends(get_redis_instance)) -> DataSchema:
    """
    Create new record.
    If record does not exist response will have 201 status code.
    Otherwise, response will have 409 status code.
    """

    if await redis.exists(request_data.phone):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Record already exist")

    await redis.set(name=request_data.phone, value=request_data.address)

    return request_data


@router.put("/write_data")
async def update_data(request_data: DataSchema, redis: Redis = Depends(get_redis_instance)) -> DataSchema:
    """
    Update record.
    If record exists response will have 200 status code.
    Otherwise, response will have 404 status code.
    """
    if not await redis.exists(request_data.phone):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Record not found")

    await redis.set(name=request_data.phone, value=request_data.address)

    return request_data
