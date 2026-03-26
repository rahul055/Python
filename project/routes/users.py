
from fastapi import APIRouter, HTTPException, Query
import logging
from typing import Optional

from services.user_service import UserService
from schemas.user import UserCreate, UserOutput


# configuration
router = APIRouter(prefix="/users", tags=["users"])

user_service = UserService()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)
logger = logging.getLogger(__name__)



@router.get('')
def get_users(
    q: Optional[str] = Query(None, description= "Search query for filtering users by name or email"),
    sort_by: Optional[str] = Query(None, description= "Sort users by age"),
    page: Optional[int] = Query(1, ge=1, description= "Page number for pagination"),
    limit: Optional[int] = Query(5, ge=1, description= "Number of users per page for pagination")
):
    try:
        logger.info("Fetching users list")
        users = user_service.get_all_users()
    
        if q:
            logger.info(f"filtering user with query: {q}")
            users = [u for u in users if q.lower() in u['name'].lower() or q.lower() in u['email'].lower()]
        if sort_by:
            try:
                users = sorted(users, key=lambda x: x.get(sort_by))
            except KeyError:
                raise HTTPException(status_code=400, detail="Invalid sort field")

        start = (page - 1) * limit
        end = start + limit
        users = users[start:end]

        return users
    
    except Exception as e:
        logger.error(f"Error fetching users: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get('/{user_id}')
def get_user_by_id(user_id: int):
    try:
        logger.info(f"Fetching user with ID: {user_id}")
        user = user_service.get_user_by_id(user_id)

        if not user:
            logger.warning(f"User with ID {user_id} not found")
            raise HTTPException(status_code=404, detail="User not found")
        
        return user

    except Exception as e:
        logger.error(f"Error fetching user with ID {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    


@router.post("", response_model=UserOutput, response_description="Create a new user")
def create_user(user: UserCreate):
    try:
        logger.info(f"Creating user with email: {user.email}")
        return user_service.add_user(user.model_dump(mode="json"))

    except Exception as e:
        logger.error(f"Error creating user: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    


@router.put("/{user_id}", response_model=UserOutput, response_description="Update user details")
def update_user(user_id: int, user: UserCreate):
    try:
        logger.info(f"Updating user with ID: {user_id}")
        updated_user = user_service.update_user(user_id, user.model_dump(mode="json"))
        if not updated_user:
            logger.warning(f"User with ID {user_id} not found")
            raise HTTPException(status_code=404, detail="User not found")
        
        return updated_user
        
    except Exception as e:
        logger.error(f"Error updating user with ID {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    


@router.delete("/{user_id}", response_description="Delete a user")
def delete_user(user_id: int):
    try:
        logger.info(f"Deleting user with ID: {user_id}")
        is_deleted = user_service.delete_user(user_id)
        if not is_deleted:
            logger.warning(f"Cannot delete user with ID: {user_id}")
            raise HTTPException(status_code=404, detail="User not found")
        return {"detail": "User deleted successfully"}
    
    except Exception as e:
        logger.error(f"Error deleting user with ID {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")