import pytesseract
import cv2
import numpy as np
import os

# --- Tesseract Configuration ---
if os.name == 'nt':  # Windows Local Testing
    windows_tesseract_path = r'C:\Users\SUPERSTAR\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'
    if os.path.exists(windows_tesseract_path):
        pytesseract.pytesseract.tesseract_cmd = windows_tesseract_path

def extract_text(image_bytes):
    """
    Enhanced OCR Engine: Upscales and processes images to capture 
    small text in screenshots.
    """
    try:
        # 1. Convert bytes to OpenCV image
        nparr = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if image is None:
            return "Error: Could not decode image."

        # 2. IMAGE SCALING (The Secret for Screenshot Accuracy)
        # We upscale the image by 2x. This makes small text (like bill amounts) 
        # much easier for Tesseract to read.
        height, width = image.shape[:2]
        image = cv2.resize(image, (width * 2, height * 2), interpolation=cv2.INTER_CUBIC)

        # 3. Preprocessing
        # Convert to Grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Denoising (Removes screenshot artifacts)
        gray = cv2.medianBlur(gray, 3)
        
        # Apply Thresholding
        processed_img = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        
        # 4. Perform OCR with PSM 3 (Automatic Page Segmentation)
        # This tells Tesseract to look for blocks of text anywhere in the image
        custom_config = r'--oem 3 --psm 3'
        text = pytesseract.image_to_string(processed_img, config=custom_config)
        
        return text.strip()

    except Exception as e:
        return f"OCR Error: {str(e)}"

if __name__ == "__main__":
    print("Enhanced OCR Engine module loaded.")