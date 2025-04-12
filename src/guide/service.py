from typing import List
from fastapi import Depends, HTTPException, status
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
    guide_id: str, author_id: str, guide: GuideModel, session: Session = Depends(get_session)
) -> Guide:
    try:
        query = select(GuideModel).where(GuideModel.id == int(guide_id))
        obj = session.exec(query).first()
        if not obj:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Note not found")
        if obj.author != author_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are unauthorized to perform this task.")
        obj.sqlmodel_update(guide)
        session.add(obj)
        session.commit()
        session.refresh(obj)
        return obj
    except Exception as e:
        raise e


async def delete_gui(guide_id: str, author_id: str, session: Session = Depends(get_session)) -> None:
    try:
        statement = session.exec(
            select(GuideModel).where(GuideModel.id == int(guide_id))
        ).first()
        if statement.author != author_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are unauthorized to perform this task.")
        session.delete(statement)
        session.commit()
    except Exception as e:
        raise e
