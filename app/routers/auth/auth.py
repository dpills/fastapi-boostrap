from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.config import settings

security = HTTPBearer()


def validate_access_token(
    access_token: HTTPAuthorizationCredentials = Security(security),
):
    """
    Validate Access Token
    """
    if access_token.credentials == settings.static_token:
        return {
            "expires_in": -1,
            "username": "admin",
        }
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")
