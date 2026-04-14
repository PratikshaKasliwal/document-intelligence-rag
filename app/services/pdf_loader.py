from pypdf import PdfReader
from fastapi import UploadFile

def extract_text_from_pdf(file: UploadFile) -> str:
    """
    Extract text from uploaded PDF.
    """
    reader = PdfReader(file.file)

    text_chunks = []
    for page in reader.pages:
        text = page.extract_text()
        if text:
            text_chunks.append(text)

    return "\n".join(text_chunks)