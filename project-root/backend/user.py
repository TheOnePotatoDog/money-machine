from fastapi import APIRouter, Depends
from .auth import get_current_user
from . import models, schemas

router = APIRouter()

@router.get("/me", response_model=schemas.UserOut)
def get_me(current_user: models.User = Depends(get_current_user)):
    """Get current user's profile (requires authentication)."""
    return current_user
