import cv2
import numpy as np
import os

def generate_shape_concept(input_folder, output_folder):
    """
    Generate shape concepts by processing images from the input folder and saving results to the output folder.

    Parameters:
    - input_folder: The folder containing input images.
    - output_folder: The folder where processed images will be saved.
    """

    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Iterate through all files in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith('.JPG') or filename.endswith('.png'):  # Adjust based on your image formats
            # Load the image
            image_path = os.path.join(input_folder, filename)
            image = cv2.imread(image_path)

            # Convert the image to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # Apply thresholding to create a binary image
            _, thresh = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)

            # Find contours in the binary image
            _, contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # Find the contour with the largest area (outer contour of the leaf)
            largest_contour = max(contours, key=cv2.contourArea)

            # Create a blank image to draw the outer contour
            contour_image = np.zeros_like(image)

            # Draw the outer contour on the blank image
            cv2.drawContours(contour_image, [largest_contour], -1, (255, 255, 255), 2)

            # Save the result in the output folder
            output_path = os.path.join(output_folder, f'outer_contour_{filename}')
            cv2.imwrite(output_path, contour_image)

            print(f"Processed {filename} and saved result as outer_contour_{filename} in {output_folder}")

    print("Processing complete.")

# Example Usage:
if __name__ == "__main__":
    input_folder = 'C:/Users/admin/Documents/PythonScripts/ontointer/main/segmentation/segmented_images/segmentedSeptoria_leaf_spot'
    output_folder = 'C:/Users/admin/Documents/PythonScripts/ontointer/main/shape/shapeConcepts/shapeSeptoria_leaf_spot'
    generate_shape_concept(input_folder, output_folder)
