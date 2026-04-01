from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from openai import OpenAI
import os

app = FastAPI()
templates = Jinja2Templates(directory="templates")


class InputData(BaseModel):
    text: str


def get_openai_client():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is not set.")
    return OpenAI(api_key=api_key)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/analyze")
async def analyze(data: InputData):
    if not data.text.strip():
        return JSONResponse(
            status_code=400,
            content={"result": "Please provide some background or interests to analyze."}
        )

    prompt = f"""
You are an AI career and learning advisor.

Given the following student background:
{data.text}

Return:
1. 2–3 possible career paths
2. Key skills they are missing
3. 2 project ideas to build those skills

Be concise, practical, and encouraging.
"""

    try:
        client = get_openai_client()
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=prompt
        )
        return {"result": response.output_text}

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"result": f"An error occurred while analyzing the input: {str(e)}"}
        )