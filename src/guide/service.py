from typing import List
from fastapi import Depends
from sqlmodel import Session, select
from config.db import get_session
from .model import Guide, GuideModel


async def all_guides(session: Session = Depends(get_session)) -> List[Guide]:
    try:
        statement = session.exec(select(GuideModel)).all()
        return statement
    except Exception as e:
        raise e


async def create(guide: GuideModel, session: Session = Depends(get_session)) -> Guide:
    try:
        obj = GuideModel.model_validate(guide)
        session.add(obj)
        session.commit()
        session.refresh(obj)
        return obj
    except Exception as e:
        raise e
    
