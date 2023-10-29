import cv2
import os
import pytesseract
from concurrent.futures import ThreadPoolExecutor

from pdf2image import convert_from_path
from pypdf import PdfMerger

from image_preprocess import noise_removal, downscale_image

from PIL import Image

Image.MAX_IMAGE_PIXELS = None


def preprocess_page(page_num, unprocessed_dir_path, processed_dir_path, extracted_dir_path):
    try:
        print(f"--- Processing page {page_num + 1}... ---")

        image = cv2.imread(unprocessed_dir_path)

        # enhanced_img = noise_removal(unprocessed_dir_path)

        # Save the processed image
        # processed_image_path = os.path.join(
        #     processed_dir_path, f"page_{page_num + 1}.png")
        # cv2.imwrite(processed_image_path, enhanced_img)

        # Perform OCR on the processed image
        extracted_text = pytesseract.image_to_string(
            image, lang='vie+eng', config="--oem 3 --psm 6")

        print("Done extracting text!")

        # if there is no text in the extracted text, skip to the next page
        if extracted_text:
            # Save the extracted text
            extracted_text_path = os.path.join(
                extracted_dir_path, f"page_{page_num + 1}.txt")
            with open(extracted_text_path, 'w', encoding='utf-8') as text_file:
                text_file.write(extracted_text)
                text_file.close()
            print("Done saving extracted text!")

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

    pages = convert_from_path(pdf_path, thread_count=4, dpi=150, grayscale=True)
    print("Done converting to images!")
    # PDF merger
    merger = PdfMerger()

    # Set up a thread pool with a specified number of workers
    with ThreadPoolExecutor(max_workers=6) as executor:
        # Process each page using thread pool
        for page_num in range(len(pages)):
            image = pages[page_num]

            # save the image
            image_path = os.path.join(
                processed_dir_path_before, f"page_{page_num}.png")
            image.save(image_path)  # Save the image as PNG

            # check if the image size is larger than 178956970
            total_pixels = image.size[0] * image.size[1]

            if total_pixels > 178956970:
                image = downscale_image(image)

            pdf_page = pytesseract.image_to_pdf_or_hocr(image, extension='pdf', lang='vie+eng',
                                                        config="--oem 3 --psm 6")
            # convert the processed images to searchable PDF
            # Save the PDF page
            pdf_page_path = f"/tmp/{page_num}.pdf"
            with open(pdf_page_path, "wb") as f:
                f.write(pdf_page)
            # Append the PDF page to the merger
            merger.append(pdf_page_path)
            os.remove(pdf_page_path)

            print("Done creating searchable!")

            executor.submit(preprocess_page, page_num, image_path,
                            processed_dir_path_after, extracted_dir_path)

        # convert the processed images to searchable PDF
        searchable_pdf_dir_with_name = os.path.join(searchable_pdf_dir, file_name + ".pdf").replace("\\", "/")

        merger.write(searchable_pdf_dir_with_name)
        merger.close()
