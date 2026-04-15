import os
import boto3
import uvicorn
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from io import BytesIO
from dotenv import load_dotenv

# Import your custom modules
from ocr_engine import extract_text
from classifier import classify_and_suggest

# Load environment variables from .env file
load_dotenv()

app = FastAPI(title="Cloud Screenshot Analyzer API")

# Enable CORS so the Frontend can talk to the Backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# AWS Configuration from Environment Variables
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
REGION_NAME = os.getenv("REGION_NAME", "us-east-1") # Default to us-east-1 if not set

# Initialize AWS S3 Client
try:
    s3_client = boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY,
        region_name=REGION_NAME
    )
except Exception as e:
    print(f"AWS Setup Error: {e}")
    s3_client = None

@app.get("/")
def home():
    return {"status": "Backend is running", "cloud_storage": "Configured" if s3_client else "Not Configured"}

@app.post("/analyze")
async def analyze_screenshot(file: UploadFile = File(...)):
    # 1. Read file contents
    try:
        contents = await file.read()
    except Exception:
        raise HTTPException(status_code=400, detail="Failed to read uploaded file")

    # 2. Upload to Cloud (AWS S3)
    # This step earns you the "Cloud Integration" marks
    s3_status = "Skipped (No Credentials)"
    if s3_client and S3_BUCKET_NAME:
        try:
            s3_client.upload_fileobj(
                BytesIO(contents), 
                S3_BUCKET_NAME, 
                file.filename,
                ExtraArgs={'ContentType': file.content_type}
            )
            s3_status = f"Successfully uploaded to S3 bucket: {S3_BUCKET_NAME}"
        except Exception as e:
            s3_status = f"S3 Upload failed: {str(e)}"
            print(s3_status)

    # 3. OCR Extraction (Text Extraction Module)
    extracted_text = extract_text(contents)
    
    if not extracted_text or not extracted_text.strip():
        return {
            "error": "No text detected in the image.",
            "cloud_status": s3_status
        }

    # 4. ML Classification (Inference Module)
    try:
        category, confidence, insight = classify_and_suggest(extracted_text)
    except Exception as e:
        print(f"ML Error: {e}")
        category, confidence, insight = "Error", "0%", "Model failed to process text."

    # 5. Return JSON Result
    return {
        "filename": file.filename,
        "text": extracted_text,
        "category": category,
        "confidence": f"{confidence:.2%}" if isinstance(confidence, float) else confidence,
        "insight": insight,
        "cloud_status": s3_status
    }

if __name__ == "__main__":
    # Run the app on port 8000
    uvicorn.run(app, host="0.0.0.0", port=8000)