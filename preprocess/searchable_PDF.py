# --- before loop ---

from PyPDF2 import PdfMerger
import pytesseract
import io

merger = PdfMerger()

file_limit = 14

output_file = "output.pdf"

# --- loop ---

for i in range(1, file_limit + 1):
    filename = "./processed_pdf/123/after/20220628 PIC-01890-22 - Phan hoi ve C3-1b/" + "page_" + str(i) + ".png"

    result = pytesseract.image_to_pdf_or_hocr(filename, lang='vie+eng', config="--oem 3")

    pdf_file_in_memory = io.BytesIO(result)
    merger.append(pdf_file_in_memory)

# --- after loop ---

merger.write(output_file)
merger.close()

# open the file using default application
import os

os.startfile(output_file)
