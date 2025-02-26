from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from . import models
from .auth import router as auth_router
from .user import router as user_router
from .ai import router as ai_router
from .payments import router as payments_router

app = FastAPI(title="Money & Safety Machine API")

# Enable CORS (allow all origins for simplicity – adjust for specific domains in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API routers with prefixes
app.include_router(auth_router, prefix="/auth")
app.include_router(user_router, prefix="/user")
app.include_router(ai_router, prefix="/ai")
app.include_router(payments_router, prefix="/payments")

# Create all database tables on startup (use Alembic for migrations in production)
Base.metadata.create_all(bind=engine)
