import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from PIL import Image
import io

def create_contract_pdf(path: str, content: str):
    """Create a PDF contract from plain text."""
    pdf_buffer = io.BytesIO()
    doc = SimpleDocTemplate(pdf_buffer, pagesize=letter, topMargin=72)
    styles = getSampleStyleSheet()
    story = []
    for line in content.split("\n"):
        if line.strip():
            story.append(Paragraph(line, styles["Normal"]))
        story.append(Spacer(1, 12))
    doc.build(story)
    pdf_buffer.seek(0)
    return pdf_buffer

def pdf_to_jpeg(pdf_buffer, output_path: str):
    """Convert first page of PDF to JPEG."""
    from pdf2image import convert_from_bytes
    images = convert_from_bytes(pdf_buffer.read(), dpi=150, first_page=1, last_page=1)
    if images:
        images[0].save(output_path, "JPEG")

os.makedirs("data/test_contracts", exist_ok=True)

orig1 = """SERVICE AGREEMENT

Section 1: Parties  
This agreement is between Alpha Corp and Beta Inc.

Section 2: Scope  
Beta Inc will provide cloud hosting services.

Section 3: Confidentiality  
Both parties agree to keep information confidential.

Section 4: Payment Terms  
4.1 Invoices are due net 15 days.  
4.2 Late payments incur a 2% monthly fee.

Section 5: Termination  
Either party may terminate with 30 days notice."""

amend1 = """SERVICE AGREEMENT

Section 1: Parties  
This agreement is between Alpha Corp and Beta Inc.

Section 2: Scope  
Beta Inc will provide cloud hosting services.

Section 3: Confidentiality  
Both parties agree to keep information confidential.

Section 4: Payment Terms  
4.1 Invoices are due net 30 days.  
4.2 Late payments incur a 1.5% monthly fee.

Section 5: Termination  
Either party may terminate with 30 days notice."""

orig2 = """NON-DISCLOSURE AGREEMENT

Section 1: Definition  
"Confidential Information" includes technical and business data.

Section 2: Obligations  
Recipient shall not disclose Confidential Information.

Section 3: Term  
This agreement shall remain in effect for 1 year from the Effective Date.

Section 4: Governing Law  
This agreement is governed by the laws of California."""

amend2 = """NON-DISCLOSURE AGREEMENT

Section 1: Definition  
"Confidential Information" includes technical and business data.

Section 2: Obligations  
Recipient shall not disclose Confidential Information.

Section 3: Term  
This agreement shall remain in effect for 2 years from the Effective Date.

Section 4: Governing Law  
This agreement is governed by the laws of California."""

contracts = [
    (orig1, "data/test_contracts/original_1.jpg"),
    (amend1, "data/test_contracts/amendment_1.jpg"),
    (orig2, "data/test_contracts/original_2.jpg"),
    (amend2, "data/test_contracts/amendment_2.jpg"),
]

try:
    for content, path in contracts:
        pdf_buf = create_contract_pdf(path, content)
        pdf_to_jpeg(pdf_buf, path)
        print(f"Generated: {path}")
except Exception as e:
    print("⚠️  To auto-generate test images, install additional dependencies:")
    print("   pip install reportlab pdf2image")
    print("   And install system package: poppler (e.g., `brew install poppler` on macOS, `apt-get install poppler-utils` on Linux)")
    print("\nAlternatively, place your own JPEG contract scans in data/test_contracts/ manually.")