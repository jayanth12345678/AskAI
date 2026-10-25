from io import BytesIO
from pypdf import PdfReader



def extract_pdf_text(content: bytes) -> dict:

    pdf_stream = BytesIO(content)
    reader = PdfReader(pdf_stream)


    pages = []

    for page in reader.pages:
        text = page.extract_text() or ""
        pages.append(text)

    full_text = "\n".join(pages)

    return {
        "page_count": len(reader.pages),
        "text": full_text
    }

