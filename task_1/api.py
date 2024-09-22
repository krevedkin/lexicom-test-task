from fastapi import APIRouter, Depends, HTTPException, status
from redis.asyncio import Redis
from deps import get_redis_instance
from schemas import DataSchema

router = APIRouter()


@router.get("/check_data/{phone}", response_model=DataSchema)
async def check_data(phone: str, redis: Redis = Depends(get_redis_instance)) -> DataSchema:
    if not phone.isdigit():
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Phone must be digit")

    address = await redis.get(name=phone)

    if not address:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Record not found")

    return DataSchema(phone=phone, address=address)


@router.post("/write_data", response_model=DataSchema)
async def create(request_data: DataSchema, redis: Redis = Depends(get_redis_instance)) -> DataSchema:
    if await redis.exists(request_data.phone):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Record already exist")

    await redis.set(name=request_data.phone, value=request_data.address)

    return request_data


@router.put("/write_data")
async def update(request_data: DataSchema, redis: Redis = Depends(get_redis_instance)) -> DataSchema:
    if not await redis.exists(request_data.phone):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Record not found")

    await redis.set(name=request_data.phone, value=request_data.address)

    return request_data
