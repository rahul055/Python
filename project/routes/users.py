
from fastapi import APIRouter, HTTPException, Query, Depends
import logging
from typing import Optional

from services.user_service import UserService
from schemas.user import UserCreate, UserOutput, UserUpdate
from database import get_db
from sqlalchemy.ext.asyncio import AsyncSession

# redis imports
from redis_client import get_redis
import redis.asyncio as redis
from services.cache_service import CacheService


# configuration
router = APIRouter(prefix="/users", tags=["users"])
logger = logging.getLogger(__name__)


def get_user_service(db: AsyncSession = Depends(get_db)) -> UserService:
    return UserService(db)

# Add a Redis dependency function (same pattern as get_user_service):
def get_cache_service(redis_client: redis.Redis = Depends(get_redis)) -> CacheService:
    return CacheService(redis_client)


@router.get('', response_model=list[UserOutput], response_description="List of users")
async def get_users(
    q: Optional[str] = Query(None, description= "Search query for filtering users by name or email"),
    page: Optional[int] = Query(1, ge=1, description= "Page number for pagination"),
    limit: Optional[int] = Query(5, ge=1, le=100, description= "Number of users per page for pagination"),
    service: UserService = Depends(get_user_service)
):
    try:
        logger.info("Fetching users list")
        return await service.get_all_users(q=q, page=page, limit=limit)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching users: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get('/{user_id}', response_model=UserOutput, response_description="Get user details by ID")
async def get_user_by_id(user_id: int, service: UserService = Depends(get_user_service), cache: CacheService = Depends(get_cache_service)):
    try:
        logger.info(f"Fetching user with ID: {user_id}")

        # check cache first
        cache_key = f"user:{user_id}"
        cached = await cache.get(cache_key)
        if cached:
            logger.info(f"Cache hit for user ID: {user_id}")
            return cached

        # if cache miss hit the database
        user = await service.get_user_by_id(user_id)
        if not user:
            logger.warning(f" User with ID {user_id} not found")
            raise HTTPException(status_code=404, detail="user not found")
        
        # 3. Store result in cache for next time (TTL: 5 min)
        output = UserOutput.model_validate(user).model_dump()
        await cache.set(cache_key, output, ttl_seconds=300)

        return user

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching user with ID {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    


@router.post("", response_model=UserOutput, status_code=201, response_description="Create a new user")
async def create_user(user: UserCreate, service: UserService = Depends(get_user_service)):
    try:
        logger.info(f"Creating user with email: {user.email}")
        return await service.create_user(user)
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating user: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    


@router.patch("/{user_id}", response_model=UserOutput, response_description="Update user details")
async def update_user(user_id: int, user: UserUpdate, service: UserService = Depends(get_user_service), cache: CacheService = Depends(get_cache_service)):
    try:
        logger.info(f"Updating user with ID: {user_id}")
        updated_user = await service.update_user(user_id, user)

        if not updated_user:
            logger.warning(f"User with ID {user_id} not found")
            raise HTTPException(status_code=404, detail="User not found")
        
        await cache.delete(f"user:{user_id}")  # Invalidate cache on update
        
        return updated_user
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating user with ID {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    


@router.delete("/{user_id}", status_code=204, response_description="Delete a user")
async def delete_user(user_id: int, service: UserService = Depends(get_user_service), cache: CacheService = Depends(get_cache_service)):
    try:
        logger.info(f"Deleting user with ID: {user_id}")
        is_deleted = await service.delete_user(user_id)

        if not is_deleted:
            logger.warning(f"Cannot delete user with ID: {user_id}")
            raise HTTPException(status_code=404, detail="User not found")
        
        await cache.delete(f"user:{user_id}")  # Invalidate cache on delete
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting user with ID {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")