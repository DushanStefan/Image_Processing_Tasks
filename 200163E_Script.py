import cv2
import numpy as np

index_number = "200163E"

# Task 1: Load an image and convert to gray-scale if necessary
image_path = '/content/IMG-20200325-WA0090.jpg'
original_image = cv2.imread(image_path)

# Check if the image was loaded correctly
if original_image is None:
    print(f"Error: Cannot load image at {image_path}.")
    exit()  # Exit the program if the image cannot be loaded

# Convert to gray-scale if the image has 3 channels
if original_image.shape[-1] == 3:
    gray_image = np.dot(original_image[..., :3], [0.2989, 0.5870, 0.1140]).astype(np.uint8)
else:
    gray_image = original_image

# Save the grayscale image
output_path = f"{index_number}_org.png"
cv2.imwrite(output_path, gray_image)
print(f"Gray-scale image saved as {output_path}")

#############################################################################################################

# Task 2: Rotate the image by 45 degrees around its center

(h, w) = gray_image.shape[:2]
center = (w // 2, h // 2)

# Create the rotation matrix using numpy
theta = np.radians(45)
cos, sin = np.cos(theta), np.sin(theta)

# Define the rotation matrix
rotation_matrix = np.array([
    [cos, -sin, center[0] * (1 - cos) + center[1] * sin],
    [sin, cos, center[1] * (1 - cos) - center[0] * sin]
])

# Calculate the new dimensions
new_w = int((h * np.abs(sin)) + (w * np.abs(cos)))
new_h = int((h * np.abs(cos)) + (w * np.abs(sin)))

# Adjust the translation for the new dimensions
rotation_matrix[0, 2] += (new_w / 2) - center[0]
rotation_matrix[1, 2] += (new_h / 2) - center[1]

# Perform the rotation using numpy
rotated_image = np.zeros((new_h, new_w), dtype=gray_image.dtype)
for i in range(new_h):
    for j in range(new_w):
        x = int((j - new_w / 2) * cos + (i - new_h / 2) * sin + center[0])
        y = int(-(j - new_w / 2) * sin + (i - new_h / 2) * cos + center[1])
        if 0 <= x < w and 0 <= y < h:
            rotated_image[i, j] = gray_image[y, x]

# Save the rotated image
cv2.imwrite(f"{index_number}_rotated.png", rotated_image)
print(f"Rotated image saved as {index_number}_rotated.png")

#############################################################################################################

# Task 3: Create an image pyramid with 5 levels
pyramid_images = [gray_image]

for level in range(1, 6):
    # Reduce the image size using numpy slicing 
    reduced_image = pyramid_images[-1][::2, ::2]
    pyramid_images.append(reduced_image)
    cv2.imwrite(f"{index_number}pyramid{level}.png", reduced_image)
    print(f"Pyramid level {level} saved as {index_number}pyramid{level}.png")

#############################################################################################################

# Task 4: Magnify the 3rd level image (25% scale) back to the original size using bilinear interpolation
third_level_image = pyramid_images[3]  # 25% scale image
scale_y, scale_x = h / third_level_image.shape[0], w / third_level_image.shape[1]

# Perform bilinear interpolation
magnified_image = np.zeros((h, w), dtype=gray_image.dtype)
for i in range(h):
    for j in range(w):
        x = j / scale_x
        y = i / scale_y

        x1 = int(np.floor(x))
        x2 = min(x1 + 1, third_level_image.shape[1] - 1)
        y1 = int(np.floor(y))
        y2 = min(y1 + 1, third_level_image.shape[0] - 1)

        # Bilinear interpolation formula
        r1 = (x2 - x) * third_level_image[y1, x1] + (x - x1) * third_level_image[y1, x2]
        r2 = (x2 - x) * third_level_image[y2, x1] + (x - x1) * third_level_image[y2, x2]
        magnified_image[i, j] = (y2 - y) * r1 + (y - y1) * r2

# Save the magnified image
magnified_output_path = f"{index_number}_mag.png"
cv2.imwrite(magnified_output_path, magnified_image)
print(f"Magnified image saved as {magnified_output_path}")

#############################################################################################################

# Task 5: Compute the difference image between the original and the magnified image using numpy
difference_image = np.abs(gray_image.astype(np.int16) - magnified_image.astype(np.int16)).astype(np.uint8)

# Save the difference image
difference_output_path = f"{index_number}_diff.png"
cv2.imwrite(difference_output_path, difference_image)
print(f"Difference image saved as {difference_output_path}")


# Task 6: Comments on the properties of the difference image

#The difference image highlights where the magnified image differs from the original. 
#Because of the downscaling and upscaling process, fine details lost during downscaling can’t be fully restored, 
#leading to noticeable differences, especially along edges and in detailed areas.
