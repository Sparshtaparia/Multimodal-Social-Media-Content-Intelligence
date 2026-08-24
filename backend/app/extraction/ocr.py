import pytesseract
from PIL import Image
from typing import List, Dict, Any, Tuple
import pandas as pd

def extract_ocr_from_image(img: Image.Image, page_num: int = 1) -> List[Dict[str, Any]]:
    """
    Extracts text blocks and bounding boxes from a single image using Tesseract OCR.
    """
    blocks = []
    
    # pytesseract image_to_data returns a dataframe-like structure with confidences and bboxes
    data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
    
    n_boxes = len(data['level'])
    current_block_text = []
    current_block_bbox = None
    confidences = []
    
    for i in range(n_boxes):
        text = data['text'][i].strip()
        conf = float(data['conf'][i])
        
        # -1 confidence means it's a structural block (page/block/par/line), not a word
        if conf != -1 and text:
            # We will group by lines or paragraphs depending on the level, but simple grouping per valid word or line works too.
            # For simplicity, if we want detailed blocks, we can treat each line as a block, or aggregate.
            # Let's just store individual non-empty words or aggregate them into lines.
            
            x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
            
            # Simple approach: save each word/phrase as a block, or aggregate lines. 
            # To keep it close to PyMuPDF, we'll store lines.
            
            # Since pytesseract already groups by block_num, par_num, line_num, word_num
            # We can just iterate and reconstruct lines.
            pass
            
    # Better approach: Group by block_num and line_num
    df = pd.DataFrame(data)
    df = df[df['conf'] != -1] # drop structural rows
    df = df[df['text'].str.strip() != ''] # drop empty text
    
    if df.empty:
        return []
        
    # Group by block and line to form text blocks
    for (block_num, line_num), group in df.groupby(['block_num', 'line_num']):
        text = " ".join(group['text'].astype(str).tolist())
        conf = group['conf'].mean() / 100.0  # Normalize to 0-1
        
        # Calculate bounding box for the line
        x0 = group['left'].min()
        y0 = group['top'].min()
        x1 = (group['left'] + group['width']).max()
        y1 = (group['top'] + group['height']).max()
        
        blocks.append({
            "page_number": page_num,
            "block_type": "text",
            "text": text,
            "bbox": [int(x0), int(y0), int(x1), int(y1)],
            "confidence": round(conf, 4),
            "source": "ocr"
        })
        
    return blocks

def process_images_ocr(images: List[Image.Image]) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    """
    Processes a list of images using OCR.
    """
    all_blocks = []
    
    for idx, img in enumerate(images):
        page_blocks = extract_ocr_from_image(img, page_num=idx + 1)
        all_blocks.extend(page_blocks)
        
    avg_conf = sum(b['confidence'] for b in all_blocks if b['block_type'] == 'text') / len([b for b in all_blocks if b['block_type'] == 'text']) if all_blocks else 0.0
        
    metadata = {
        "page_count": len(images),
        "ocr_used": True,
        "extraction_method": "Tesseract",
        "average_ocr_confidence": round(avg_conf, 4)
    }
    
    return all_blocks, metadata
