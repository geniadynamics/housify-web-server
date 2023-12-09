from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

router = APIRouter()


fake_users_db = {
    "user@example.com": {
        "email": "user@example.com",
        "password": "password123",
        "refresh_token": "fake_refresh_token",
    }
}


class TokenRefreshRequest:
    def __init__(self, refresh_token: str):
        self.refresh_token = refresh_token


@router.post("/refresh")
def refresh_token(request: TokenRefreshRequest, token: str = Depends(OAuth2PasswordBearer(tokenUrl="token"))):
    """
    Update an access token using a refresh token.

    Parameters:
    - `request`: Token update data (refresh_token).
    - `token`: Current access token (required as part of the header).

    Returns:
    - New access token.
    """
    user = fake_users_db.get("user@example.com")
    if user and user["refresh_token"] == request.refresh_token:

        new_access_token = "fake_new_access_token"
        return {"token": new_access_token, "token_type": "bearer"}
    else:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
