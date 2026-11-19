import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import engine, Base, SessionLocal
from app.core.exceptions import register_exception_handlers
from app.api import compounds, categories, search, references, aera

logger = logging.getLogger("aethera.main")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Ensure database schema is ready
    try:
        Base.metadata.create_all(bind=engine)
        # Check if database is empty on fresh PostgreSQL deployment, auto-populate if so
        from app.models.models import Compound
        from app.seed import seed_database
        with SessionLocal() as db:
            if db.query(Compound).count() == 0:
                logger.info("Fresh database detected. Auto-seeding initial molecular dataset...")
                seed_database()
    except Exception as e:
        logger.warning(f"Database startup check note: {e}")
    yield

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Enterprise Clean Architecture API for Aethera AI",
    version="1.0.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc",
    lifespan=lifespan
)

# Set up CORS middleware
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Register custom global exceptions
register_exception_handlers(app)

# Include API Routers
app.include_router(compounds.router, prefix=settings.API_V1_STR)
app.include_router(categories.router, prefix=settings.API_V1_STR)
app.include_router(search.router, prefix=settings.API_V1_STR)
app.include_router(references.router, prefix=settings.API_V1_STR)
app.include_router(aera.router, prefix=settings.API_V1_STR)

@app.get("/")
def read_root():
    return {
        "status": "online",
        "service": settings.PROJECT_NAME,
        "docs": f"{settings.API_V1_STR}/docs"
    }

@app.get("/health")
@app.get(f"{settings.API_V1_STR}/health")
def health_check():
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME
    }
