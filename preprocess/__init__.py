import time
import os
from PyPDF2 import PdfReader
from pdf_preprocess import preprocess_pdf
import shutil


# Set up the directories
raw_pdf_dir = "/Users/nitieii/LNT + MRB Sharing Dropbox/CP05"
processed_pdf_dir = "preprocess/processed_pdf"
extracted_text_dir = "preprocess/extracted_pdf"

# remove the directories if they exist
shutil.rmtree(processed_pdf_dir)
shutil.rmtree(extracted_text_dir)

# Create the directories if they don't exist
os.makedirs(processed_pdf_dir, exist_ok=True)
os.makedirs(extracted_text_dir, exist_ok=True)


start_time = time.time()

for root, dirs, files in os.walk(raw_pdf_dir):
    for file in files:
        # Check if the file is a PDF file, not empty, not hidden, not processed, and not protected
        if file.endswith(".pdf") and os.stat(os.path.join(root, file)).st_size != 0 and not file.startswith('.') and not os.path.exists(os.path.join(processed_pdf_dir, os.path.splitext(file)[0])) and not os.path.exists(os.path.join(extracted_text_dir, os.path.splitext(file)[0])) and not PdfReader(open(os.path.join(root, file), 'rb')).is_encrypted:
            print(f"Processing {file}...")
            preprocess_pdf(os.path.join(root, file),
                           processed_pdf_dir, extracted_text_dir)
            print(f"Finished processing {file}")

end_time = time.time()
execution_time = end_time - start_time

print(f"Total execution time: {execution_time} seconds")
