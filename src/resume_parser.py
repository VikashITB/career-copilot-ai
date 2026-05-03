"""
resume_parser.py – Extract plain text from uploaded PDF or DOCX resume files.
"""

import io
from typing import Optional
import streamlit as st


def parse_pdf(file_bytes: bytes) -> str:
    """
    Extract text from a PDF file given as raw bytes.
    Uses PyPDF2; falls back gracefully if a page cannot be decoded.
    """
    try:
        import PyPDF2
    except ImportError:
        raise ImportError("PyPDF2 is required: pip install PyPDF2")

    reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
    pages: list[str] = []
    for page in reader.pages:
        try:
            text = page.extract_text() or ""
            pages.append(text)
        except Exception:
            pages.append("")
    return "\n".join(pages)


def parse_docx(file_bytes: bytes) -> str:
    """
    Extract text from a DOCX file given as raw bytes.
    Iterates over paragraphs and table cells.
    """
    try:
        from docx import Document
    except ImportError:
        raise ImportError("python-docx is required: pip install python-docx")

    doc = Document(io.BytesIO(file_bytes))
    parts: list[str] = []

    # Paragraphs
    for para in doc.paragraphs:
        if para.text.strip():
            parts.append(para.text)

    # Tables
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                if cell.text.strip():
                    parts.append(cell.text)

    return "\n".join(parts)


def parse_resume(uploaded_file) -> Optional[str]:
    """
    Parse a Streamlit UploadedFile object (PDF or DOCX).
    Returns extracted plain text, or None on failure.
    
    Parameters
    ----------
    uploaded_file : streamlit.runtime.uploaded_file_manager.UploadedFile
        The file object from st.file_uploader.
    """
    if uploaded_file is None:
        return None

    file_bytes = uploaded_file.read()
    name = uploaded_file.name.lower()

    try:
        if name.endswith(".pdf"):
            return parse_pdf(file_bytes)
        elif name.endswith(".docx"):
            return parse_docx(file_bytes)
        elif name.endswith(".txt"):
            return file_bytes.decode("utf-8", errors="replace")
        else:
            st.error("Unsupported file type. Please upload a PDF, DOCX, or TXT file.")
            return None
    except Exception as exc:
        st.error(f"Failed to parse resume: {exc}")
        return None
