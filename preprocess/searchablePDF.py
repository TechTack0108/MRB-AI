from PyPDF2 import PdfMerger
import os
import pytesseract


def create_searchable_pdf(image, output_path: str, page_num: int, merger: PdfMerger):
    """Generate a searchable PDF from document images.
    """

    # Convert the image to a PDF page
    pdf_page = pytesseract.image_to_pdf_or_hocr(image, extension='pdf', lang='vie+eng')
    # Save the PDF page
    pdf_page_path = f"/tmp/{page_num}.pdf"
    with open(pdf_page_path, "wb") as f:
        f.write(pdf_page)

    # Append the PDF page to the merger
    merger.append(pdf_page_path)
    os.remove(pdf_page_path)

    print("Done!")
    return None
