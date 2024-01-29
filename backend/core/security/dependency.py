from jose import jwt
from jose.exceptions import JOSEError
from fastapi import HTTPException, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from backend.core.config.env import env

security = HTTPBearer()

async def has_access(credentials: HTTPAuthorizationCredentials= Depends(security)):
    """
        Function that is used to validate the token in the case that it requires it
    """
    token = credentials.credentials

    try:
        payload = jwt.decode(token, key=env.JWT_SECRET, options={"verify_signature": True,
                                                           "verify_aud": False,
                                                           "verify_iss": False})
        return payload
    except JOSEError as e:  # catches any exception
        raise HTTPException(
            status_code=401,
            detail=str(e))