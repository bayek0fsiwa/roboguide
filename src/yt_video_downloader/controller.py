from fastapi import APIRouter, Request


router = APIRouter()


@router.post("")
async def downloader(req: Request):
    body = await req.json()
    link = body.get("link")
    return link
