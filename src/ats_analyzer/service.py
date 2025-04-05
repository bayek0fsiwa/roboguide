import os
import re
from google import genai
from dotenv import load_dotenv
from pypdf import PdfReader


load_dotenv()
GEMINI_KEY: str = os.getenv("GEMINI_KEY")
client = genai.Client(api_key=GEMINI_KEY)


def analyze_resume(resume_path: str):
    reader = PdfReader(resume_path)
    page = reader.pages[0]
    contents = page.extract_text()
    # contents = ""
    # with open(resume_path, "rb") as f:
    #     contents = f.read()
    prompt = """
    you are a ATS resume analyzer. You will receive content from resume and
    you need to analyze and suggest the improvements and what could have been done better.
    and give response in json format.
    """
    # uploaded_file = client.files.upload(file=resume_path)
    response = client.models.generate_content(
        model="gemini-2.0-flash", contents=f"{prompt}: Here is the content to analyze - {contents}"
    )
    result = response.text
    re.sub("\n  ", "", result)
    return response.text
