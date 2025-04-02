from typing import List
from fastapi import APIRouter, Request, HTTPException, status, Depends
from sqlmodel import Session, select
from .model import Guide, GuideModel
from config.db import get_session
from .service import all_guides, create


router = APIRouter()


@router.get('', status_code=200)
async def get_all_guides(session: Session = Depends(get_session)) -> List[Guide]:
    return await all_guides(session)


@router.post('', status_code=201)
async def create_guide(req: Request, session: Session = Depends(get_session)) -> Guide:
    data = await req.json()
    return await create(data, session)


@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
async def update_guide(req: Request, session: Session = Depends(get_session)) -> Guide:
    guide_id = req.path_params["id"]
    statement = session.exec(select(GuideModel).where(GuideModel.id == int(guide_id))).first()
    if not statement:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Guide not found.")
    data = await req.json()
    GuideModel.model_validate(data)
    statement.title = data["title"]
    statement.description = data["description"]
    statement.author = data["author"]
    session.add(statement)
    session.commit()
    session.refresh(statement)
    return statement


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_guide(req: Request, session: Session = Depends(get_session)) -> None:
    guide_id = req.path_params["id"]
    statement = session.exec(select(GuideModel).where(GuideModel.id == int(guide_id))).first()
    if not statement:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Guide not found.")
    session.delete(statement)
    session.commit()
