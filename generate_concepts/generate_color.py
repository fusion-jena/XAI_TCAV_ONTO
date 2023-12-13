from PIL import Image, ImageDraw
import os
import numpy as np

def generate_color_concept(target_color, output_directory, colors=None, std_deviation=1.5, num_images=30, image_width=256, image_height=256):
    """
    Generate colored images with random color changes and save them to specified directories.

    Parameters:
    - target_color: A string representing the color name to generate images for.
    - output_directory: The base directory where color-specific folders will be created.
    - colors: A dictionary containing color names as keys and RGB tuples as values.
    - std_deviation: Standard deviation for random color changes (default is 1.5).
    - num_images: Number of images to generate for each color (default is 30).
    - image_width: Width of the generated images (default is 256).
    - image_height: Height of the generated images (default is 256).
    """

    if colors is None:
        colors = {
            "Black": (0, 0, 0),
            "Brown": (123, 63, 0),
            "DarkBrown": (101, 67, 33),
            "LightGreen": (144, 238, 144),
            "Yellow": (255, 255, 0),
            "Gray": (128, 128, 128),
            "White": (255, 255, 255),
            "DarkGreen": (0, 100, 0),
            "YellowishGreen": (154, 205, 50),
            "GrayWhite": (192, 192, 192),
            "LightBrown": (205, 133, 63),
            "ReddishBrown": (139, 69, 19),
            "Purple": (128, 0, 128)
        }

    if target_color not in colors:
        raise ValueError(f"Color '{target_color}' not found in the provided colors dictionary.")

    target_color_rgb = colors[target_color]

    color_folder = os.path.join(output_directory, target_color)
    os.makedirs(color_folder, exist_ok=True)

    for i in range(num_images):
        # Generate random color changes with small standard deviation for each RGB component
        color_changes = np.random.normal(0, std_deviation, 3).astype(int)
        new_color = tuple(np.clip(c + change, 0, 255) for c, change in zip(target_color_rgb, color_changes))

        # Create a new image with the specified dimensions and color
        image = Image.new('RGB', (image_width, image_height), new_color)

        # Save the image with a unique filename indicating intensity
        filename = f"{target_color.lower().replace(' ', '_')}_{i + 1}.png"
        image_path = os.path.join(color_folder, filename)
        image.save(image_path)

        print(f"Image {i + 1} for {target_color} saved as {filename} in {color_folder}")

    print("Image generation complete.")


