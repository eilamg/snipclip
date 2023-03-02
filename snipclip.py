import io
import os
import subprocess

import pyclip
import pytesseract
from PIL import Image, ImageGrab


TEXT_CLEANUP = str.maketrans({
    '“': '"',
    '”': '"',
    "’": "'",
    "‘": "'"
})



if 'tesseract' not in os.getenv('PATH', ''):
    with open(os.path.join(os.path.dirname(__file__), 'TESSERACT_PATH')) as f:
        tesseract_path = f.read().strip()
    pytesseract.pytesseract.tesseract_cmd = tesseract_path


def convert_image_format(image: Image.Image, output_format: str) -> Image.Image:
    """Convert PIL image from one format to another in-memory."""
    buffer = io.BytesIO()
    image.save(buffer, output_format)
    converted_image = Image.open(buffer)
    return converted_image


def snipclip():
    """Capture part of the screen, run contents through OCR and return text."""
    subprocess.run('snippingtool /clip')
    image = ImageGrab.grabclipboard()
    image = convert_image_format(image, 'BMP')
    text = pytesseract.image_to_string(image).translate(TEXT_CLEANUP)
    return text


if __name__ == '__main__':
    pyclip.copy(snipclip())
