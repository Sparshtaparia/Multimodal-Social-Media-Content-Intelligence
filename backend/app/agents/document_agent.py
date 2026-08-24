from typing import List, Dict, Any, Tuple
from pathlib import Path
from PIL import Image

from app.extraction.pdf import is_scanned_pdf, extract_native_pdf, render_pdf_to_images
from app.extraction.ocr import process_images_ocr

def process_document(file_path: str, file_type: str) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    """
    Takes a file path and routes it to the correct extraction strategy.
    Returns (blocks, metadata).
    """
    
    with open(file_path, "rb") as f:
        file_bytes = f.read()

    if file_type == "pdf":
        import fitz
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        
        if is_scanned_pdf(doc):
            print("PDF detected as scanned. Falling back to OCR.")
            images = render_pdf_to_images(file_bytes)
            return process_images_ocr(images)
        else:
            print("PDF detected as native text. Using PyMuPDF.")
            return extract_native_pdf(file_bytes)
            
    else:
        # It's an image
        print("Image detected. Using Tesseract OCR.")
        img = Image.open(io.BytesIO(file_bytes))
        # Ensure it's in a format Tesseract likes
        if img.mode != 'RGB':
            img = img.convert('RGB')
        blocks, metadata = process_images_ocr([img])
        # Add image block spanning the full image
        blocks.insert(0, {
            "page_number": 1,
            "block_type": "image",
            "text": None,
            "bbox": [0, 0, img.width, img.height],
            "confidence": 1.0,
            "source": "uploaded_image"
        })
        metadata["page_width"] = img.width
        metadata["page_height"] = img.height
        return blocks, metadata

import io # needed for the Image.open(io.BytesIO) above
