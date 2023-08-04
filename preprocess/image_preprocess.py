import cv2
import numpy as np


def noise_removal(image):
    try:
        # Check if the image is already in grayscale
        if len(image.shape) > 2 and image.shape[2] == 3:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Apply noise removal techniques
        kernel = np.ones((1, 1), np.uint8)
        dilated_image = cv2.dilate(image, kernel, iterations=1)
        eroded_image = cv2.erode(dilated_image, kernel, iterations=1)
        opened_image = cv2.morphologyEx(eroded_image, cv2.MORPH_OPEN, kernel)
        denoised_image = cv2.medianBlur(opened_image, 3)

        # Binarize the image
        thresh, im_bw = cv2.threshold(
            denoised_image, 210, 230, cv2.THRESH_BINARY)

        print("Noise removal done.")
        # Thicker the text
        im_bw = cv2.erode(im_bw, kernel, iterations=1)

        return im_bw
    except Exception as e:
        return print("Error in noise_removal: ", e)


def enhance_image(image):
    try:
        # Convert image to grayscale if necessary
        if len(image.shape) > 2 and image.shape[2] == 3:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Apply contrast enhancement
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        contrast_enhanced_image = clahe.apply(image)

        return contrast_enhanced_image
    except Exception as e:
        return print("Error in enhanced_image: ", e)
