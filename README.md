# Image Manipulation Pipeline

This code processes an image through several steps:

1. **Convert to Grayscale**: The original image is converted to grayscale and saved.
2. **Rotate the Image**: The image is rotated by 45 degrees around its center and saved.
3. **Image Pyramid**: An image pyramid is created with 5 levels by progressively reducing the image size and saving each level.
4. **Magnify Image**: The 3rd level image (25% of the original size) is magnified back to the original size using bilinear interpolation and saved.
5. **Difference Image**: The difference between the original grayscale image and the magnified image is calculated and saved.
6. **Comment on Difference**: The difference image highlights changes after downscaling and upscaling, showing discrepancies mainly in fine details and edges.

Each processed image is saved with a specific filename based on the index number.
