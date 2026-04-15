import easyocr
import fitz  # PyMuPDF
from PIL import Image
import numpy as np

def extract_text_from_pdf(pdf_path):
    """Extracts text from each page of a PDF."""
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()
    return text

def extract_text_from_image(image_file):
    """Extracts text from an image using OCR."""
    reader = easyocr.Reader(['en'])
    # Convert uploaded file to format EasyOCR likes
    img = Image.open(image_file)
    text_results = reader.readtext(np.array(img), detail=0)
    return " ".join(text_results)