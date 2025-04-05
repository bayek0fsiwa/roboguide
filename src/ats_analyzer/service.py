import os
from google import genai
from dotenv import load_dotenv

load_dotenv()
GEMINI_KEY: str = os.getenv("GEMINI_KEY")
client = genai.Client(api_key=GEMINI_KEY)


def analyze_resume(resume_path: str):
    contents = ""
    with open(resume_path, "r") as f:
        contents = f.read()
    prompt = """
    you are a ATS resume analyzer. You will receive content from resume and
    you need to analyze and suggest the improvements and what could have been done better.
    """
    response = client.models.generate_content(
        model="gemini-2.0-flash", contents=f"{prompt}: Here is the content to analyze - {contents}"
    )

    return response.text
