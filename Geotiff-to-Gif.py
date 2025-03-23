import os
import rasterio
import numpy as np
import imageio.v2 as imageio
from rasterio.windows import Window
from google.colab import drive  # Only needed if running in Google Colab

# Authenticate and mount Google Drive (Remove if not using Google Colab)
try:
    import ee
    ee.Authenticate()
    drive.mount("/content/drive")
except ImportError:
    print("Google Earth Engine not available. Make sure you are running this in Colab if needed.")

# Define paths
INPUT_FOLDER = "/content/drive/MyDrive/Timeseries"
OUTPUT_CROPPED_FOLDER = "/content/drive/MyDrive/cropped_images"
OUTPUT_GIF = "/content/drive/MyDrive/timelapse_cropped.gif"
FPS = 2

# Create output directory if it doesn't exist
os.makedirs(OUTPUT_CROPPED_FOLDER, exist_ok=True)

# Get sorted list of GeoTIFF files
tif_files = sorted(
    [os.path.join(INPUT_FOLDER, f) for f in os.listdir(INPUT_FOLDER) if f.endswith(".tif")]
)

if not tif_files:
    raise FileNotFoundError("No GeoTIFF files found in the specified folder!")

# Determine the smallest image dimensions
min_width, min_height = float("inf"), float("inf")
for file_path in tif_files:
    with rasterio.open(file_path) as src:
        min_width = min(min_width, src.width)
        min_height = min(min_height, src.height)

# Define crop window based on the smallest dimensions
def crop_region(src):
    crop_window = Window(0, 0, min_width, min_height)
    cropped_image = src.read(window=crop_window)
    return cropped_image

cropped_images = []

# Process each image
for i, file_path in enumerate(tif_files):
    with rasterio.open(file_path) as src:
        cropped_img = crop_region(src)
        cropped_images.append(cropped_img)
        
        # Normalize to 8-bit and convert to RGB
        img_8bit = np.uint8(255 * (cropped_img - np.min(cropped_img)) / (np.max(cropped_img) - np.min(cropped_img)))
        img_8bit_rgb = np.stack([img_8bit[0]] * 3, axis=0)
        
        # Save the cropped image
        output_path = os.path.join(OUTPUT_CROPPED_FOLDER, f"cropped_{i+1}.png")
        imageio.imwrite(output_path, img_8bit_rgb.transpose(1, 2, 0))

print(f"All images cropped and saved to {OUTPUT_CROPPED_FOLDER}")

# Generate GIF
cropped_files = sorted(
    [os.path.join(OUTPUT_CROPPED_FOLDER, f) for f in os.listdir(OUTPUT_CROPPED_FOLDER) if f.endswith(".png")]
)

with imageio.get_writer(OUTPUT_GIF, mode="I", fps=FPS) as writer:
    for file_path in cropped_files:
        image = imageio.imread(file_path)
        writer.append_data(image)

print(f"Timelapse GIF saved as {OUTPUT_GIF}")
