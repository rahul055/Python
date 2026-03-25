import datetime
from fastapi import APIRouter, HTTPException
import json
from pydantic import BaseModel
import logging


# configuration
router = APIRouter(prefix="/users", tags=["users"])

# configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)
logger = logging.getLogger(__name__)

# load users from a JSON file
with open('data/users.json', 'r') as f:
    users = json.load(f)


# define a Pydantic model for creating a new user
class CreateUserRequest(BaseModel):
    name: str
    age: int
    email: str
    phone: str
    address: str


@router.get("")
def get_users():
    try:
        return {"users": users}
    
    except Exception as e:
        logger.error(f"Error occurred while fetching users: {e}")
        raise HTTPException(status_code=500, detail="internal server error")



@router.get("/adults")
def get_adults():
    try:
        adults = [ u for u in users if u['age'] >= 18] if users else []
        logger.info(f"Adults found: {len(adults)}")
        if not adults:
            raise HTTPException(status_code=404, detail="No adults found")
        return { "adults": adults }
    
    except Exception as e:
        logger.error(f"Error occurred while fetching adults: {e}")
        raise HTTPException(status_code=500, detail="internal server error")



@router.get("/{name}")
def get_user_by_name(name: str):
    try:
        user = next(( u for u in users if u['name'].lower() == name.lower()), None)
        logger.info(f"User search for name: {name} - Found: {user is not None}")
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return {"user": user}
    
    except Exception as e:
        logger.error(f"Error occurred while searching for user: {e}")
        raise HTTPException(status_code=500, detail="internal server error")




@router.post("")
def create_user(user: CreateUserRequest):
    try:
        get_latest_id = max([u['id'] for u in users]) if users else 0

        logger.info(f"Creating user with ID: {get_latest_id + 1}")
        new_user = {
            "id": get_latest_id + 1,
            "created_at": datetime.datetime.now().isoformat(),
            **user.model_dump()
        }

        users.append(new_user)
        logger.info(f"User created: {new_user['id']}")
        with open('data/users.json', 'w') as f:
            json.dump(users, f, indent=4)

        if not new_user:
            raise HTTPException(status_code=400, detail="Failed to create user")
        
        logger.info(f"User created successfully: {new_user['id']}")
        return { "user": new_user }
    
    except Exception as e:
        logger.error(f"Error occurred while creating user: {e}")
        raise HTTPException(status_code=500, detail="internal server error")