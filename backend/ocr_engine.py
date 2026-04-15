import pytesseract
import cv2
import numpy as np
import os

# --- Tesseract Configuration ---
# If running on Windows, we point to the .exe file.
# On AWS/Linux, 'tesseract' is usually in the system PATH, so we don't need to set this.
if os.name == 'nt':  # 'nt' means Windows
    # Default installation path for Tesseract on Windows
    windows_tesseract_path = r'C:\Users\SUPERSTAR\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'
    
    if os.path.exists(windows_tesseract_path):
        pytesseract.pytesseract.tesseract_cmd = windows_tesseract_path
    else:
        print("ERROR: Tesseract OCR not found at C:\\Program Files\\Tesseract-OCR. "
              "Please install it or update the path in ocr_engine.py")

def extract_text(image_bytes):
    """
    Takes image bytes, processes the image for better OCR accuracy,
    and returns the extracted text.
    """
    try:
        # 1. Convert bytes to a numpy array for OpenCV
        nparr = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if image is None:
            return "Error: Could not decode image."

        # 2. Preprocessing for better OCR accuracy
        # Convert to Grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply Thresholding (makes text stand out)
        # Using OTSU thresholding which automatically finds the best threshold value
        processed_img = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        
        # 3. Perform OCR
        text = pytesseract.image_to_string(processed_img)
        
        return text.strip()

    except Exception as e:
        return f"OCR Error: {str(e)}"

# This block allows you to test this specific file individually
if __name__ == "__main__":
    print("OCR Engine module loaded.")