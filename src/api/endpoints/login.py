from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

router = APIRouter()

fake_users_db = {
    "user@example.com": {
        "email": "user@example.com",
        "password": "password123",
    }
}


class LoginRequest:
    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password


@router.post("/login")
def login(request: LoginRequest, token: str = Depends(OAuth2PasswordBearer(tokenUrl="token"))):
    """
    Perform authentication and generate an access token.

    Parameters:
    - `request`: Login credentials (username and password).
    - `token`: Authentication token (required as part of the header).

    Returns:
    - Success or error message.
    """
    user = fake_users_db.get(request.email)
    if user and user["password"] == request.password:
        return {"token": token, "token_type": "bearer"}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")
