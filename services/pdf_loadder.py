"""
services/pdf_loadder.py

Utility for extracting raw text from an uploaded resume PDF.
"""

from pypdf import PdfReader


def extract_text_from_pdf(uploaded_pdf) -> str:
    """
    Extract text from an uploaded PDF file (e.g. a Streamlit
    UploadedFile object or any file-like object accepted by pypdf).

    Returns an empty string if no text could be extracted
    (for example, a scanned/image-only PDF).
    """

    reader = PdfReader(uploaded_pdf)

    text_chunks = []

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:
            text_chunks.append(page_text)

    return "\n".join(text_chunks)
