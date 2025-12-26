from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class TextRequest(BaseModel):
    text: str

@app.get("/")
def read_root():
    return {"status": "online", "version": "1.0.0"}

@app.post("/analyze")
def analyze_text(request: TextRequest):
    if not request.text:
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    # Simulating a logic check
    word_count = len(request.text.split())
    is_question = request.text.strip().endswith("?")
    
    return {
        "word_count": word_count,
        "is_question": is_question,
        "processed": True
    }