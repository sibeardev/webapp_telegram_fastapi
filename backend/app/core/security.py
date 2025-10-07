import hashlib
import hmac
import logging
from datetime import datetime, timedelta
from typing import Optional
from urllib.parse import parse_qsl

from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY
from jose import jwt

logger = logging.getLogger(__name__)


def create_access_token(user_id: str, expires_delta: Optional[timedelta] = None):
    expire = datetime.now() + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode = {"sub": str(user_id), "exp": expire}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def validate_telegram_init_data(init_data: str, bot_token: str) -> bool:
    vals = dict(parse_qsl(init_data, strict_parsing=True))
    check_hash = vals.pop("hash", None)
    if not check_hash:
        return False
    data_check_string = "\n".join(
        f"{key}={value}" for key, value in sorted(vals.items())
    )
    secret_key = hmac.new(
        "WebAppData".encode(), bot_token.encode(), hashlib.sha256
    ).digest()
    hmac_hash = hmac.new(
        secret_key, data_check_string.encode(), hashlib.sha256
    ).hexdigest()

    return hmac_hash == check_hash
