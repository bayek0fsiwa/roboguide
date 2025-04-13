import io
import pathlib  # , json
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlmodel import Session

from config.db import get_session
from middleware.auth_middleware import get_current_user

from .model import Guide

# from config.reddish import redis_client as r
from .service import all_guides, create, delete_gui, update

router = APIRouter()
BASE_DIR = pathlib.Path(__file__).cwd()
UPLOADS_DIR = BASE_DIR / "uploads"
UPLOADS_DIR.mkdir(exist_ok=True)


@router.get("", status_code=status.HTTP_200_OK)
async def get_all_guides(session: Session = Depends(get_session)) -> List[Guide]:
    try:
        data = await all_guides(session)
        # cached_data = r.get("all_guides")
        # if cached_data is not None:
        #     return json.loads(cached_data)
        # r.setex("all_guides", 3600 ,json.dumps(data))
        return data
    except Exception as e:
        raise e


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_guide(
    req: Request,
    session: Session = Depends(get_session),
    user=Depends(get_current_user),
):
    try:
        data = await req.form()
        title = data["title"]
        description = data["description"]
        author = data["author"]
        img_file = UPLOADS_DIR / str(data["img"].filename)
        with open(img_file, "wb") as out:
            out.write(io.BytesIO(await data["img"].read()).read())
        base_url = req.base_url
        image_location = img_file.name
        image_path = f"{base_url}code/{UPLOADS_DIR.name}/{image_location}"
        to_save = {
            "title": title,
            "description": description,
            "img": image_path,
            "author": user.get("sub"),
        }
        # print(user)
        return await create(to_save, session)
    except Exception as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, f"{e}")


@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
async def update_guide(
    req: Request,
    session: Session = Depends(get_session),
    user=Depends(get_current_user),
):
    try:
        guide_id = req.path_params["id"]
        data = await req.form()
        author_id = user.get("sub")
        title = data["title"]
        description = data["description"]
        img_file = UPLOADS_DIR / str(data["img"].filename)
        with open(img_file, "wb") as out:
            out.write(io.BytesIO(await data["img"].read()).read())
        base_url = req.base_url
        image_location = img_file.name
        image_path = f"{base_url}code/{UPLOADS_DIR.name}/{image_location}"
        to_save = {
            "title": title,
            "description": description,
            "img": image_path,
            "author": author_id,
        }
        return await update(guide_id, author_id, to_save, session)
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"{e}")


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_guide(
    req: Request,
    session: Session = Depends(get_session),
    user=Depends(get_current_user),
) -> None:
    try:
        author_id = user.get("sub")
        guide_id = req.path_params["id"]
        await delete_gui(guide_id, author_id, session)
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"{e}")
