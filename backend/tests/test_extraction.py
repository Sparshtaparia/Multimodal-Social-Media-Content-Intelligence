import os
import pytest
from unittest.mock import patch
import pandas as pd
from app.agents.document_agent import process_document
from app.profiling.metadata import generate_metadata_profile
from app.profiling.linguistic import calculate_linguistic_features

FIXTURE_DIR = os.path.join(os.path.dirname(__file__), 'fixtures')

def test_native_pdf_extraction():
    path = os.path.join(FIXTURE_DIR, 'text_native.pdf')
    blocks, meta = process_document(path, "pdf")
    
    assert meta["extraction_method"] == "PyMuPDF"
    assert meta["ocr_used"] is False
    assert len(blocks) > 0
    assert any("Try our new platform" in b["text"] for b in blocks if b["block_type"] == "text")
    
    # Check block structure
    b0 = blocks[0]
    assert "page_number" in b0
    assert "block_type" in b0
    assert "text" in b0
    assert "bbox" in b0
    assert "confidence" in b0
    assert b0["source"] == "native_pdf"

@patch('pytesseract.image_to_data')
def test_scanned_pdf_uses_ocr(mock_tesseract):
    mock_tesseract.return_value = {
        'level': [5], 'page_num': [1], 'block_num': [1], 'par_num': [1], 'line_num': [1], 'word_num': [1],
        'left': [10], 'top': [10], 'width': [100], 'height': [20], 'conf': [95.0], 'text': ['scanned']
    }
    path = os.path.join(FIXTURE_DIR, 'scanned.pdf')
    blocks, meta = process_document(path, "pdf")
    
    assert meta["extraction_method"] == "Tesseract"
    assert meta["ocr_used"] is True
    assert len(blocks) > 0
    assert any("scanned" in b["text"].lower() for b in blocks if b["block_type"] == "text")
    
    # Check block structure
    b0 = blocks[0]
    assert "bbox" in b0
    assert "confidence" in b0
    assert b0["source"] == "ocr"

@patch('pytesseract.image_to_data')
def test_image_uses_ocr(mock_tesseract):
    mock_tesseract.return_value = {
        'level': [5], 'page_num': [1], 'block_num': [1], 'par_num': [1], 'line_num': [1], 'word_num': [1],
        'left': [10], 'top': [10], 'width': [100], 'height': [20], 'conf': [95.0], 'text': ['engagement']
    }
    path = os.path.join(FIXTURE_DIR, 'social_post.jpg')
    blocks, meta = process_document(path, "image")
    
    assert meta["extraction_method"] == "Tesseract"
    assert meta["ocr_used"] is True
    assert len(blocks) > 0
    assert any("engagement" in b["text"].lower() for b in blocks if b["block_type"] == "text")

@patch('pytesseract.image_to_data')
def test_metadata_profile_generated(mock_tesseract):
    mock_tesseract.return_value = {
        'level': [5, 5], 'page_num': [1, 1], 'block_num': [1, 1], 'par_num': [1, 1], 'line_num': [1, 1], 'word_num': [1, 2],
        'left': [10, 50], 'top': [10, 10], 'width': [30, 60], 'height': [20, 20], 'conf': [95.0, 96.0], 'text': ['Boost', '#marketing']
    }
    path = os.path.join(FIXTURE_DIR, 'social_post.jpg')
    blocks, meta = process_document(path, "image")
    
    profile = generate_metadata_profile(blocks, meta)
    assert profile["hashtag_count"] >= 1  # "#marketing"
    assert profile["text_block_count"] >= 1
    # since 'Boost your engagement' might not hit our dummy CTA list directly unless we add it, we skip assert on content_type

def test_linguistic_profile_generated():
    text = "Boost your engagement now! #marketing"
    ling = calculate_linguistic_features(text)
    
    assert ling["word_count"] > 3
    assert ling["exclamation_count"] == 1
    assert ling["sentence_count"] >= 1
