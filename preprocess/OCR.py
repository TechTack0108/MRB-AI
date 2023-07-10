import cv2
import os
import pytesseract

extracted_dir_path = "extracted_pdf"


def extract_text_from_file(file, file_name):
    image = cv2.imread(file)

    extracted_text = pytesseract.image_to_string(
        image, lang='vie+eng', config='--oem 1 --psm 3')

    # create the directory if it doesn't exist
    os.makedirs(os.path.join(extracted_dir_path, file_name), exist_ok=True)

    # Save the extracted text
    extracted_text_path = os.path.join(
        extracted_dir_path, file_name, "page_1.txt")

    with open(extracted_text_path, 'w', encoding='utf-8') as text_file:
        text_file.write(extracted_text)


for root, dirs, files in os.walk("processed_pdf"):
    for file in files:
        if file.endswith(".png"):
            # get the parent folder of the file
            file_name = root.split('/')[-1]

            print(f"Extracting text from {file_name}...")
            extract_text_from_file(os.path.join(root, file), file_name)

            print(f"Finished extracting text from {file}")
        else:
            continue
