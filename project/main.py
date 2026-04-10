from fastapi import FastAPI
import logging

from contextlib import asynccontextmanager
from database import engine, Base
from routes.users import router as users_router 
from config import get_settings
from redis_client import get_redis

# configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)
logger = logging.getLogger(__name__)
settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # create tables on startup
    logger.info("Creating database tables...")

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database tables created successfully")

    r = get_redis()
    await r.ping() # type: ignore
    logger.info("Connected to Redis successfully")

    yield # app runs here

    logger.info("Shutting down: closing database connection...")
    await engine.dispose()


app = FastAPI(
    title=settings.APP_NAME,
    lifespan=lifespan,
    debug=settings.DEBUG
)

app.include_router(users_router, prefix="/api/v1")

@app.get("/health", response_description="Health check endpoint")
def health_check():
    return {"status": "healthy", "app_name": settings.APP_NAME}