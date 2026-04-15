from fastapi import FastAPI, UploadFile, File
from ocr_engine import extract_text
from classifier import classify_and_suggest
import uvicorn

app = FastAPI()

@app.post("/analyze")
async def analyze_screenshot(file: UploadFile = File(...)):
    contents = await file.read()
    
    # 1. OCR
    extracted_text = extract_text(contents)
    
    if not extracted_text.strip():
        return {"error": "No text detected in image"}

    # 2. ML Classification
    category, confidence, insight = classify_and_suggest(extracted_text)
    
    return {
        "text": extracted_text,
        "category": category,
        "confidence": f"{confidence:.2%}",
        "insight": insight
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)