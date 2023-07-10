from image_preprocess import noise_removal, enhance_image
import pytesseract
import cv2
import numpy as np
import os
from concurrent.futures import ThreadPoolExecutor
from pdf2image import convert_from_path
from memory_profiler import profile


@profile
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

        # only extract the text from the header of the page
        # header_extracted_text = pytesseract.image_to_string(

        # Perform OCR on the processed image
        extracted_text = pytesseract.image_to_string(
            nonoise_image, lang='eng', config='--oem 1 --psm 3')

        # Save the extracted text
        extracted_text_path = os.path.join(
            extracted_dir_path, f"page_{page_num+1}.txt")
        with open(extracted_text_path, 'w', encoding='utf-8') as text_file:
            text_file.write(extracted_text)
            text_file.close()

    except Exception as e:
        return print("Error in preprocess_page: ", e)


@profile
def get_kv_map(blocks):
    key_map = {}
    value_map = {}
    block_map = {}
    for block in blocks:
        block_id = block['Id']
        block_map[block_id] = block
        if block['BlockType'] == "KEY_VALUE_SET" and 'KEY' in block['EntityTypes']:
            key_map[block_id] = block
        else:
            value_map[block_id] = block
    return key_map, value_map, block_map


@profile
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
