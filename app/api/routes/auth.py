from datetime import timedelta
from typing import Annotated

from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, HTTPException, Depends


from app.core import security
from app.api.deps import SessionDep
from app.core.config import settings
from app.users.schemas import Token
from app.users import services

router = APIRouter()


@router.post("/token")
async def get_auth_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: SessionDep) -> Token:
    user = await services.authenticate(
        session=session, username=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=400)
    elif not user.is_active:
        raise HTTPException(status_code=400)

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return Token(
        access_token=security.create_access_token(
            user.id, expires_delta=access_token_expires
        )
    )

