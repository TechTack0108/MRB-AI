import cv2
import os
import pytesseract
from concurrent.futures import ThreadPoolExecutor
from pdf2image import convert_from_path
from searchablePDF import create_searchable_pdf
from PyPDF2 import PdfMerger


# from image_preprocess import noise_removal, enhance_image


def preprocess_page(page_num, image_path, processed_dir_path, extracted_dir_path):
    try:
        print(f"--- Processing page {page_num + 1}... ---")

        # Load the image
        image = cv2.imread(image_path)

        # # Check if the image is loaded successfully
        # if image is None:
        #     print(f"Error loading image: {image_path}")
        #     return
        #
        # # Apply noise removal techniques
        # nonoise_image = noise_removal(image)
        # nonoise_image = enhance_image(nonoise_image)

        # Save the processed image
        processed_image_path = os.path.join(
            processed_dir_path, f"page_{page_num + 1}.png")

        cv2.imwrite(processed_image_path, image)

        # Perform OCR on the processed image
        extracted_text = pytesseract.image_to_string(
            image, lang='vie+eng', config="--oem 3")

        # Save the extracted text
        extracted_text_path = os.path.join(
            extracted_dir_path, f"page_{page_num + 1}.txt")
        with open(extracted_text_path, 'w', encoding='utf-8') as text_file:
            text_file.write(extracted_text)
            text_file.close()

    except Exception as e:
        return print("Error in preprocess_page: ", e)


def preprocess_pdf(pdf_path, processed_pdf_dir, extracted_text_dir, searchable_pdf_dir):
    # Extract the file name and create the corresponding directories
    file_name = os.path.splitext(os.path.basename(pdf_path))[0]
    processed_dir_path_before = os.path.join(processed_pdf_dir, "before", file_name).replace("\\", "/")
    processed_dir_path_after = os.path.join(processed_pdf_dir, "after", file_name).replace("\\", "/")
    extracted_dir_path = os.path.join(extracted_text_dir, file_name).replace("\\", "/")

    # create the directories if they don't exist
    os.makedirs(processed_dir_path_before, exist_ok=True)
    os.makedirs(processed_dir_path_after, exist_ok=True)
    os.makedirs(extracted_dir_path, exist_ok=True)

    # PDF merger
    # merger = PdfMerger()

    # Convert the first PDF page to image
    pages = convert_from_path(pdf_path)

    # Set up a thread pool with a specified number of workers
    with ThreadPoolExecutor(max_workers=6) as executor:
        # Process each page using thread pool
        for page_num in range(len(pages)):
            image = pages[page_num]
            image_path = os.path.join(
                processed_dir_path_before, f"page_{page_num}.png")
            image.save(image_path)  # Save the image as PNG
            executor.submit(preprocess_page, page_num, image_path,
                            processed_dir_path_after, extracted_dir_path)

            # convert the processed images to searchable PDF
        #     searchable_pdf_dir_with_name = os.path.join(searchable_pdf_dir, file_name + ".pdf").replace("\\", "/")
        #
        #     create_searchable_pdf(image, searchable_pdf_dir_with_name, page_num, merger)
        # merger.close()
