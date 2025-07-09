import logging
from contextlib import asynccontextmanager

from config import config
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

logger = logging.getLogger(__name__)
logging.basicConfig(level=config.log_level.value.upper())


@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- Startup ---
    logger.info("Starting application...")

    # DATABASE CONNECTION

    yield

    # --- Shutdown ---
    logger.info("Shutting down application...")

    # Placeholder: Close database or other async services here
    # await close_db()


app = FastAPI(title=config.app_name, debug=config.debug, lifespan=lifespan)

# CORS Setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "ok", "environment": config.environment.value}


# Include your API routers here
