import cv2
import numpy as np


def noise_removal(image):
    try:
        # Load the image
        image = cv2.imread(image)

        # Convert to grayscale
        # gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        #
        # # Resize to 1191x2000 pixels
        # resized_img = cv2.resize(gray_img, (1191, 2000))

        # Apply unsharp mask
        blurred_img = cv2.GaussianBlur(image, (0, 0), 6.8)
        unsharp_img = cv2.addWeighted(image, 1.0 + 2.69, blurred_img, -0.69, 0)

        print("Noise removal done.")
        # Thicker the text
        # im_bw = cv2.erode(im_bw, kernel, iterations=1)

        return unsharp_img
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


def downscale_image(image):
    # Convert the PIL Image to a numpy array
    image_np = np.array(image)

    # downscale the image to a value less than 178956970
    total_pixels = image_np.shape[0] * image_np.shape[1]

    scale_percent = 178956970 / total_pixels
    width = int(image_np.shape[1] * scale_percent)
    height = int(image_np.shape[0] * scale_percent)
    dim = (width, height)

    # resize image
    resized_image = cv2.resize(image_np, dim, interpolation=cv2.INTER_AREA)
    return resized_image
