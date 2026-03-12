from fastapi import Depends, Header, HTTPException
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import decode_token
from app.db.session import get_db


def get_db_dep(db: Session = Depends(get_db)) -> Session:
    return db


def get_admin_user(authorization: str | None = Header(default=None)) -> str:
    if not authorization or not authorization.startswith('Bearer '):
        raise HTTPException(status_code=401, detail='Unauthorized')
    token = authorization.replace('Bearer ', '')
    sub = decode_token(token)
    if sub != settings.admin_email:
        raise HTTPException(status_code=401, detail='Invalid token')
    return sub
