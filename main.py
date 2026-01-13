from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
import os

app = FastAPI()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

class AnalyzeRequest(BaseModel):
    prompt: str

@app.post("/analyze")
def analyze(req: AnalyzeRequest):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Отвечай кратко и по делу."},
            {"role": "user", "content": req.prompt}
        ],
        max_tokens=500
    )

    return {
        "result": response.choices[0].message.content
    }
