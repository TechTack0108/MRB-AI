from image_preprocess import noise_removal, enhance_image
import pytesseract
import cv2
import re
import os
from concurrent.futures import ThreadPoolExecutor
from pdf2image import convert_from_path
from deskew import deskew


def preprocess_page(page_num, image_path, processed_dir_path, extracted_dir_path):
    try:
        print(f"--- Processing page {page_num+1}... ---")

        # Load the image
        image = cv2.imread(image_path)

        # Check if the image is loaded successfully
        if image is None:
            print(f"Error loading image: {image_path}")
            return

        # deskewed_image = deskew(image)

        # Apply noise removal techniques
        nonoise_image = noise_removal(image)
        nonoise_image = enhance_image(nonoise_image)

        # Save the processed image
        processed_image_path = os.path.join(
            processed_dir_path, f"page_{page_num+1}.png")

        cv2.imwrite(processed_image_path, nonoise_image)

        # # Perform OCR on the processed image
        extracted_text = pytesseract.image_to_string(
            nonoise_image, lang='vie', config='--oem 1 --psm 3')

        # Remove newline characters, punctuation, and unnecessary characters
        # extracted_text = re.sub(r'\n', ' ', extracted_text)

        # Save the extracted text
        extracted_text_path = os.path.join(
            extracted_dir_path, f"page_{page_num+1}.txt")
        with open(extracted_text_path, 'w', encoding='utf-8') as text_file:
            text_file.write(extracted_text)
    except Exception as e:
        return print("Error in preprocess_page: ", e)


def preprocess_pdf(pdf_path, processed_pdf_dir, extracted_text_dir):
    # Extract the file name and create the corresponding directories
    file_name = os.path.splitext(os.path.basename(pdf_path))[0]
    processed_dir_path = os.path.join(processed_pdf_dir, file_name)
    extracted_dir_path = os.path.join(extracted_text_dir, file_name)
    os.makedirs(processed_dir_path, exist_ok=True)
    os.makedirs(extracted_dir_path, exist_ok=True)

    # Convert the PDF pages to images
    pages = convert_from_path(pdf_path)

    # Set up a thread pool with a specified number of workers
    with ThreadPoolExecutor(max_workers=8) as executor:
        # Process each page using thread pool
        # for page_num in range(len(pages)):
        image = pages[0]
        image_path = os.path.join(
            processed_dir_path, f"page_{1}.png")
        image.save(image_path)  # Save the image as PNG
        executor.submit(preprocess_page, 0, image_path,
                        processed_dir_path, extracted_dir_path)
