from fastapi import APIRouter, Request, HTTPException, status, Depends
from sqlmodel import Session, select
from .model import Auth, AuthModel
from config.db import get_session


router = APIRouter()


@router.get('', status_code=201)
def register_user(session: Session = Depends(get_session)) -> Auth:
    statement = session.exec(select(AuthModel)).all()
    return statement


@router.post('', status_code=200)
async def login_user(req: Request, session: Session = Depends(get_session)) -> Auth:
    data = await req.json()
    obj = AuthModel.model_validate(data)
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj
