import os
import re
from pdf2image import convert_from_path
import pytesseract

# Configuración Tesseract
pytesseract.pytesseract.tesseract_cmd = "/opt/homebrew/bin/tesseract"
os.environ["TESSDATA_PREFIX"] = "/opt/homebrew/Cellar/tesseract-lang/4.1.0/share/tessdata"

def clean_text(text):
    text = re.sub(r'\x0c', '', text)
    text = re.sub(r'[\u200b-\u200f\u202a-\u202e]', '', text)
    return text.strip()

def extract_text_from_pdf(pdf_path):
    """Extrae texto del PDF con OCR"""
    try:
        pages = convert_from_path(pdf_path, 400)  # Mejor resolución
        full_text = ""
        for i, page in enumerate(pages):
            text = pytesseract.image_to_string(page, lang="spa")
            full_text += f"--- Página {i+1} ---\n{clean_text(text)}\n\n"
        return full_text
    except Exception as e:
        raise RuntimeError(f"Error al extraer texto: {str(e)}")