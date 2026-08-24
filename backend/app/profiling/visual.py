from typing import List, Dict, Any

def generate_visual_profile(blocks: List[Dict[str, Any]], extraction_metadata: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generates a visual profile by analyzing bounding boxes of blocks.
    Calculates text area, image area, and their ratios to the page size.
    """
    # Assuming page dimensions are provided or we estimate from max coordinates
    # In PyMuPDF we can get this, but for now we estimate based on max block extents if not available
    max_x = 0
    max_y = 0
    
    text_area = 0.0
    image_area = 0.0
    
    headline_detected = False
    
    for b in blocks:
        bbox = b.get("bbox")
        if not bbox or len(bbox) != 4:
            continue
            
        x0, y0, x1, y1 = bbox
        width = max(0, x1 - x0)
        height = max(0, y1 - y0)
        area = width * height
        
        max_x = max(max_x, x1)
        max_y = max(max_y, y1)
        
        if b.get("block_type") == "text":
            text_area += area
            
            # Simple heuristic for headline: large text block near the top of the page
            # We assume a block is a headline if it's in the top 20% of the known y-space and reasonably large
            if y0 < (max_y * 0.2 if max_y > 0 else 200) and height > 20:
                headline_detected = True
                
        elif b.get("block_type") == "image":
            image_area += area

    # Default to 800x600 if no blocks have valid coords
    page_width = extraction_metadata.get("page_width", max_x if max_x > 0 else 800)
    page_height = extraction_metadata.get("page_height", max_y if max_y > 0 else 600)
    
    total_page_area = page_width * page_height
    
    text_area_ratio = text_area / total_page_area if total_page_area > 0 else 0.0
    image_area_ratio = image_area / total_page_area if total_page_area > 0 else 0.0
    
    # Calculate density (ratio of bounding box text area to page area)
    text_density = text_area_ratio
    
    return {
        "text_area": text_area,
        "image_area": image_area,
        "text_area_ratio": round(text_area_ratio, 4),
        "image_area_ratio": round(image_area_ratio, 4),
        "text_density": round(text_density, 4),
        "headline_detected": headline_detected
    }
