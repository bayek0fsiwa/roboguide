import pathlib, io#, json
from typing import List
from fastapi import APIRouter, Request, status, Depends
from sqlmodel import Session
from .model import Guide
from config.db import get_session
# from config.reddish import redis_client as r
from .service import all_guides, create, update, delete_gui


router = APIRouter()
BASE_DIR = pathlib.Path(__file__).cwd()
UPLOADS_DIR = BASE_DIR / "uploads"
UPLOADS_DIR.mkdir(exist_ok=True)


@router.get('', status_code=status.HTTP_200_OK)
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



@router.post('', status_code=status.HTTP_201_CREATED)
async def create_guide(req: Request, session: Session = Depends(get_session)):
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
    to_save = {"title": title, "description": description, "img": image_path, "author": author}
    return await create(to_save , session)


@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
async def update_guide(req: Request, session: Session = Depends(get_session)) -> Guide:
    guide_id = req.path_params["id"]
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
    to_save = {"title": title, "description": description, "img": image_path, "author": author}
    return await update(guide_id, to_save, session)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_guide(req: Request, session: Session = Depends(get_session)) -> None:
    guide_id = req.path_params["id"]
    await delete_gui(guide_id, session)
