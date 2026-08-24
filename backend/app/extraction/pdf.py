import io
from typing import List, Dict, Any, Tuple
import fitz  # PyMuPDF
from PIL import Image

def is_scanned_pdf(doc: fitz.Document) -> bool:
    """
    Heuristic to determine if a PDF is mostly scanned (requires OCR).
    If text length is very low compared to the number of pages, we assume it's scanned.
    """
    total_text = ""
    for page in doc:
        total_text += page.get_text()
    
    if len(total_text.strip()) < 50 and len(doc) > 0:
        return True
    return False

def extract_native_pdf(file_bytes: bytes) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    """
    Extracts text blocks and metadata natively using PyMuPDF.
    Returns (blocks, metadata).
    """
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    
    blocks = []
    page_count = len(doc)
    
    for page_num in range(page_count):
        page = doc[page_num]
        page_dict = page.get_text("dict")
        
        for block in page_dict.get("blocks", []):
            if block.get("type") == 0:  # text block
                text_content = ""
                for line in block.get("lines", []):
                    for span in line.get("spans", []):
                        text_content += span.get("text", "") + " "
                
                text_content = text_content.strip()
                if text_content:
                    blocks.append({
                        "page_number": page_num + 1,
                        "block_type": "text",
                        "text": text_content,
                        "bbox": block.get("bbox"),  # [x0, y0, x1, y1]
                        "confidence": 1.0,  # Native extraction is assumed 100% accurate for what's there
                        "source": "native_pdf"
                    })
            elif block.get("type") == 1: # image block
                blocks.append({
                    "page_number": page_num + 1,
                    "block_type": "image",
                    "text": None,
                    "bbox": block.get("bbox"),
                    "confidence": 1.0,
                    "source": "native_pdf"
                })
                
    metadata = {
        "page_count": page_count,
        "ocr_used": False,
        "extraction_method": "PyMuPDF"
    }
    
    return blocks, metadata

def render_pdf_to_images(file_bytes: bytes) -> List[Image.Image]:
    """
    Renders PDF pages to PIL Images for OCR.
    """
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    images = []
    
    # Zoom factor for better OCR resolution (e.g. 300 DPI approx)
    zoom = 2.0
    mat = fitz.Matrix(zoom, zoom)
    
    for page in doc:
        pix = page.get_pixmap(matrix=mat)
        img = Image.open(io.BytesIO(pix.tobytes("png")))
        images.append(img)
        
    return images
