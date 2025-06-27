from fpdf import FPDF
import os

def create_downloadable_pdf(content, title="Document"):
    """
    Generates a downloadable, ATS-friendly PDF from text content using fpdf2.
    This method has no external C-library dependencies.
    """
    pdf = FPDF()
    pdf.add_page()

    # Define the path to the font file
    font_path = os.path.join("assets", "DejaVuSans.ttf")
    
    # Check if the font file exists before adding it
    if not os.path.exists(font_path):
        raise FileNotFoundError(
            f"Font file not found at {font_path}. "
            "Please download DejaVuSans.ttf and place it in the 'assets' folder."
        )

    # Add a Unicode font that supports a wide range of characters
    pdf.add_font('DejaVu', '', font_path, uni=True)
    pdf.set_font('DejaVu', '', 11)

    # Use multi_cell to automatically handle text wrapping
    # w=0 means it will use the full page width (minus margins)
    pdf.multi_cell(0, 5, content)

    # Return the PDF content as bytes. Use 'latin-1' encoding as fpdf2 suggests.
    return pdf.output(dest='S').encode('latin-1')