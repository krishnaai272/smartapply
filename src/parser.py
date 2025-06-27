import io
import pypdf
import docx

def parse_resume(file):
    """
    Parses an uploaded resume file (PDF, DOCX, or TXT) and returns its text content.
    """
    filename = file.name
    try:
        if filename.endswith(".pdf"):
            return parse_pdf(file)
        elif filename.endswith(".docx"):
            return parse_docx(file)
        elif filename.endswith(".txt"):
            return file.getvalue().decode("utf-8")
        else:
            return "Error: Unsupported file format. Please upload a PDF, DOCX, or TXT file."
    except Exception as e:
        return f"Error parsing file: {e}"

def parse_pdf(file):
    """Helper function to parse a PDF file."""
    pdf_reader = pypdf.PdfReader(io.BytesIO(file.getvalue()))
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() or ""
    return text

def parse_docx(file):
    """Helper function to parse a DOCX file."""
    doc = docx.Document(io.BytesIO(file.getvalue()))
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text