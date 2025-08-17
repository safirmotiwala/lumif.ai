
import uvicorn
from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from utilities.logger import get_logger
from config import settings
from chat.route import router as ChatRouter
from tools.route import router as ToolsRouter
from dotenv import load_dotenv

logger = get_logger(__name__)
load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 Server has started successfully!")
    yield
    logger.info("🛑 Server is shutting down...")

app = FastAPI(
    title=settings.TITLE,
    description=settings.DESCRIPTION,
    version=settings.BUILD,
    docs_url='/docs',
    openapi_url='/openapi.json',
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["Root"])
def read_root():
    """A simple root endpoint to confirm the API is running."""
    return {
        "status": "ok",
        "version": settings.BUILD,
        "development": settings.DEVELOPMENT,
        "host": settings.HOST,
        "port": settings.PORT,
        "title": settings.TITLE,
        "description": settings.DESCRIPTION,
        "docs": settings.DOCS_URL,
        "openapi": settings.OPENAPI_URL
    }


router = APIRouter(prefix="/v1")
router.include_router(ChatRouter)
router.include_router(ToolsRouter)

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT, reload=settings.DEVELOPMENT)