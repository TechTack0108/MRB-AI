import os
import pytesseract
import psutil
from concurrent.futures import ThreadPoolExecutor
from pdf2image import convert_from_path
from pypdf import PdfMerger
from PIL import Image

Image.MAX_IMAGE_PIXELS = None

# Function to get CPU usage percentage

# Set the maximum allowed CPU usage percentage
max_cpu_usage = 75  # Adjust this value as needed


def get_cpu_usage():
    return psutil.cpu_percent(interval=1)


width, height = 800, 1200


def preprocess_page(page_num, image, processed_dir_path, extracted_dir_path):
    try:
        print(f"--- Processing page {page_num + 1}... ---")

        # Resize image to an optimal size
        image = image.resize((width, height), Image.ANTIALIAS)

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
            print("Done saving extracted text!")

        # convert to searchable PDF
        pdf_page = pytesseract.image_to_pdf_or_hocr(image, extension='pdf', lang='vie+eng',
                                                    config="--oem 3 --psm 6")
        # convert the processed images to searchable PDF
        # Save the PDF page
        pdf_page_path = f"/tmp/{page_num}.pdf"
        with open(pdf_page_path, "wb") as f:
            f.write(pdf_page)

        print("Done creating searchable PDF page!")

        return pdf_page_path

    except Exception as e:
        print(f"Error processing page {page_num}: {e}")
        return None


def preprocess_pdf(pdf_path, processed_pdf_dir, extracted_text_dir, searchable_pdf_dir, lang='vie+eng',
                   initial_batch_size=10):
    try:
        # Extract the file name and create the corresponding directories
        file_name = os.path.splitext(os.path.basename(pdf_path))[0]
        processed_dir_path_before = os.path.join(processed_pdf_dir, "before", file_name).replace("\\", "/")
        processed_dir_path_after = os.path.join(processed_pdf_dir, "after", file_name).replace("\\", "/")
        extracted_dir_path = os.path.join(extracted_text_dir, file_name).replace("\\", "/")

        # create the directories if they don't exist
        os.makedirs(processed_dir_path_before, exist_ok=True)
        os.makedirs(processed_dir_path_after, exist_ok=True)
        os.makedirs(extracted_dir_path, exist_ok=True)

        # Convert PDF pages to images
        pages = convert_from_path(pdf_path, thread_count=4, dpi=150, grayscale=True, hide_annotations=True)
        print("Done converting to images!")

        # Get the total number of pages in the PDF
        total_pages = len(pages)

        # Set up a thread pool with an optimal number of workers
        max_workers = psutil.cpu_count(logical=False) or 1  # Use physical cores if available, otherwise use 1
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            pdf_page_paths = []  # List to store processed PDF pages

            batch_size = initial_batch_size

            for batch_start in range(0, total_pages, batch_size):
                batch_end = min(batch_start + batch_size, total_pages)
                batch_pages = pages[batch_start:batch_end]

                # Process each page in the batch using thread pool
                batch_futures = []
                for page_num, image in enumerate(batch_pages, start=batch_start):
                    # Check CPU usage before processing each page in the batch
                    current_cpu_usage = get_cpu_usage()
                    print(f"Current CPU usage: {current_cpu_usage}%")
                    if current_cpu_usage >= max_cpu_usage:
                        print(f"CPU usage reached {current_cpu_usage}%, reducing batch size for the current page.")
                        batch_size = max(1, batch_size // 2)  # Reduce batch size by half for the current page

                    future = executor.submit(preprocess_page, page_num, image, processed_dir_path_after,
                                             extracted_dir_path)
                    batch_futures.append(future)

                # Wait for all pages in the batch to be processed
                batch_pdf_page_paths = [future.result() for future in batch_futures if future.result() is not None]
                pdf_page_paths.extend(batch_pdf_page_paths)

            # Continue with PDF merging even if CPU usage threshold was exceeded
            if pdf_page_paths:
                # PDF merger
                merger = PdfMerger()
                for pdf_page_path in pdf_page_paths:
                    # Append the PDF page to the merger
                    merger.append(pdf_page_path)
                    os.remove(pdf_page_path)

                # convert the processed images to searchable PDF
                searchable_pdf_dir_with_name = os.path.join(searchable_pdf_dir, file_name + ".pdf").replace("\\", "/")

                merger.write(searchable_pdf_dir_with_name)
                merger.close()
                print("Searchable PDF created successfully.")
            else:
                print("No pages were processed. Searchable PDF not created.")

    except Exception as e:
        print("Error in preprocess_pdf: ", e)
