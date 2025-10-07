from app.core.config import ALGORITHM, SECRET_KEY
from bot.models import User
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt

security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user = await User.get(payload.get("sub"))
        if not user:
            raise HTTPException(status_code=401)
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
