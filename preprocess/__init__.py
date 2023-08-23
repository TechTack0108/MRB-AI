import os
import sys
from PyPDF2 import PdfReader

from pdf_preprocess import preprocess_pdf

current_dir = os.path.dirname(os.path.realpath(__file__))
mrb_ai_dir = os.path.dirname(current_dir)

download_id = "123"

# Set up the directories
raw_pdf_dir = mrb_ai_dir + "/files/" + download_id
processed_pdf_dir = current_dir + "/processed_pdf/" + download_id
extracted_text_dir = current_dir + "/extracted_pdf/" + download_id

# # remove the directories if they exist
# shutil.rmtree(processed_pdf_dir)
# shutil.rmtree(extracted_text_dir)

# Create the directories if they don't exist
os.makedirs(processed_pdf_dir, exist_ok=True)
os.makedirs(extracted_text_dir, exist_ok=True)

for root, dirs, files in os.walk(raw_pdf_dir):
    for file in files:
        # Check if the file is a PDF file, not empty, not hidden, not processed, and not protected, not color
        if file.endswith(".pdf") and os.stat(os.path.join(root, file)).st_size != 0 and not file.startswith(
                '.') and not os.path.exists(
            os.path.join(processed_pdf_dir, os.path.splitext(file)[0])) and not os.path.exists(
            os.path.join(extracted_text_dir, os.path.splitext(file)[0])):
            print(f"Processing {file}...")
            preprocess_pdf(os.path.join(root, file),
                           processed_pdf_dir, extracted_text_dir)
            print(f"Finished processing {file}")
