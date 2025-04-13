# import re
from google import genai
from pypdf import PdfReader

from config.configs import settings

client = genai.Client(api_key=settings.GEMINI_KEY)


def cleanup(content: str) -> str:
    # return re.sub(["\\n\\n", '\\'], ' ', content)
    return content.replace("\\n\\n", " ").replace("\\", " ")


def analyze_resume(resume_path: str) -> str:
    reader = PdfReader(resume_path)
    page = reader.pages[0]
    contents = page.extract_text()
    prompt = """
    you are a ATS resume analyzer. You will receive content from resume and
    you need to analyze and suggest the improvements and what could have been done better.
    and give response in list format and do not use special characters likr *, \, new line character or extra spaces.
    """
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=f"{prompt}: Here is the content to analyze - {contents}",
    )
    result = response.text
    return cleanup(result)
