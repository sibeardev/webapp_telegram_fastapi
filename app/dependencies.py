from typing import Annotated

from fastapi import Header, HTTPException, status

from app.settings import X_TOKEN


async def get_token_header(x_token: Annotated[str, Header()]):
    if x_token != X_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="X-Token header invalid"
        )
