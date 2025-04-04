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


async def update(
    guide_id: str, guide: GuideModel, session: Session = Depends(get_session)
) -> Guide:
    try:
        statement = session.exec(
            select(GuideModel).where(GuideModel.id == int(guide_id))
        ).first()
        GuideModel.model_validate(guide)
        statement.title = guide["title"]
        statement.description = guide["description"]
        statement.img = guide["img"]
        statement.author = guide["author"]
        session.add(statement)
        session.commit()
        session.refresh(statement)
        return statement
    except Exception as e:
        raise e


async def delete_gui(guide_id: str, session: Session = Depends(get_session)) -> None:
    try:
        statement = session.exec(
            select(GuideModel).where(GuideModel.id == int(guide_id))
        ).first()
        session.delete(statement)
        session.commit()
    except Exception as e:
        raise e
