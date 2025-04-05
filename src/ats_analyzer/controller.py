import io
import pathlib
from fastapi import APIRouter, HTTPException, Request, status

from ats_analyzer.service import analyze_resume


router = APIRouter()
BASE_DIR = pathlib.Path(__file__).cwd()
UPLOADS_DIR = BASE_DIR / "uploads"
UPLOADS_DIR.mkdir(exist_ok=True)


@router.post('')
async def anaylyzer(req: Request):
    try:
        form_data = await req.form()
        file_type = form_data["resume"].content_type
        if file_type is not "application/pdf":
            raise Exception("Please provide pdf file only.")
        res_file = UPLOADS_DIR / str(form_data["resume"].filename)
        with open(res_file, "wb") as out:
            out.write(io.BytesIO(await form_data["resume"].read()).read())
        return analyze_resume(res_file)
    except Exception as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, f"{e}")
