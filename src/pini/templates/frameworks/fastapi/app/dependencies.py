from app.utils.authentication import decode_access_token
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)  # Adjust if needed


def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    payload = decode_access_token(token)
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )
    return {"user_id": user_id}  # Can be expanded to real user model later


# Sample usage in a FastAPI router
"""
from fastapi import APIRouter, Depends
from app.dependencies import get_current_user

router = APIRouter(prefix="/protected", tags=["Protected"])


@router.get("/dashboard")
async def protected_dashboard(current_user: dict = Depends(get_current_user)):
    return {"message": f"Welcome user {current_user['user_id']}"}
"""
