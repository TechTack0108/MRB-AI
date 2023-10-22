import os
import pytesseract
from pdf2image import convert_from_path
from pypdf import PdfMerger


def create_searchable_pdf():
    """Generate a searchable PDF from document images.
    """
    try:
        file_name = "DLM-MLT-00001-22-EV.pdf"
        merger = PdfMerger()
        current_dir = os.getcwd()
        input_path = os.path.join(current_dir, "unprocessed_files", file_name).replace("\\", "/")
        pages = convert_from_path(input_path, thread_count=4)
        print("Processing pages: " + str(len(pages)))

        file_name = os.path.splitext(os.path.basename(input_path))[0]
        print("file_name: " + file_name)

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

            print("Done creating searchable for page: " + str(page_num))

        if not os.path.exists(os.path.join(current_dir, "ocr")):
            os.makedirs(os.path.join(current_dir, "ocr"), exist_ok=True)

        # convert the processed images to searchable PDF
        searchable_pdf_dir_with_name = os.path.join(current_dir, "ocr", file_name + ".pdf").replace("\\", "/")

        merger.write(searchable_pdf_dir_with_name)
        merger.close()

    except Exception as e:
        print(f"An error occurred: {str(e)}")
