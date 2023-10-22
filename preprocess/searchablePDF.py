import os

from pypdf import PdfMerger
import pytesseract
from pdf2image import convert_from_path


def create_searchable_pdf(input_path: str):
    """Generate a searchable PDF from document images.
    """
    merger = PdfMerger()
    pages = convert_from_path(input_path, thread_count=4)

    file_name = os.path.splitext(os.path.basename(input_path))[0]

    for page_num in range(len(pages)):
        image = pages[page_num]

        pdf_page = pytesseract.image_to_pdf_or_hocr(image, extension='pdf', lang='vie+eng', config="--oem 3")
        # convert the processed images to searchable PDF
        # Save the PDF page
        pdf_page_path = f"/tmp/{page_num}.pdf"
        with open(pdf_page_path, "wb") as f:
            f.write(pdf_page)
        # Append the PDF page to the merger
        merger.append(pdf_page_path)
        os.remove(pdf_page_path)

        print("Done creating searchable for page: !" + str(page_num))

    if not os.path.exists("ocr"):
        os.makedirs("ocr", exist_ok=True)

    # convert the processed images to searchable PDF
    searchable_pdf_dir_with_name = os.path.join("ocr", file_name + ".pdf").replace("\\", "/")

    merger.write(searchable_pdf_dir_with_name)
    merger.close()
