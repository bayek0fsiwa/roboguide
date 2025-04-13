from fastapi import Depends
from sqlmodel import Session

from auth.model import AuthModel
from config.db import get_session


async def save_to_db(data: AuthModel, session: Session = Depends(get_session)):
    try:
        obj = AuthModel.model_validate(data)
        session.add(obj)
        session.commit()
        session.refresh(obj)
        return obj
    except Exception as e:
        raise e
