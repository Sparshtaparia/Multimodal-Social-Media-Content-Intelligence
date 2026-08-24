import fitz
from PIL import Image, ImageDraw, ImageFont

def generate_text_native_pdf(path: str):
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((50, 50), "Try our new platform today.\nLearn more by clicking the link.")
    doc.save(path)
    doc.close()

def generate_scanned_pdf(path: str):
    # Create an image with text, then convert to PDF to simulate a scan
    img = Image.new('RGB', (400, 200), color='white')
    d = ImageDraw.Draw(img)
    d.text((10,10), "This is a scanned document.", fill=(0,0,0))
    # We save to PDF directly via PIL
    img.save(path, "PDF", resolution=100.0)

def generate_social_image(path: str):
    img = Image.new('RGB', (400, 200), color='white')
    d = ImageDraw.Draw(img)
    d.text((10,10), "Boost your engagement now! #marketing", fill=(0,0,0))
    img.save(path)

if __name__ == "__main__":
    generate_text_native_pdf("tests/fixtures/text_native.pdf")
    generate_scanned_pdf("tests/fixtures/scanned.pdf")
    generate_social_image("tests/fixtures/social_post.jpg")
