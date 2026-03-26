from fastapi import FastAPI
import logging

from routes.users import router as users_router


# app configuration
app = FastAPI()

# configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)
logger = logging.getLogger(__name__)

# include the users router
app.include_router(users_router)

@app.get('/')
def read_root():
    return {"message": "Welcome to the API"}