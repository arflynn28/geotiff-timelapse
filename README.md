# GeoTIFF Time Series to Timelapse GIF  

This repository contains a Python script that processes GeoTIFF time series imagery, crops all images based on the smallest file in the dataset, converts them to 8-bit RGB format, and generates an animated GIF to visualize changes over time. 

## How to Use
1 Place your GeoTIFF images in the data/ folder or specify your own directory.
2️ Run the script: Geotiff-to-Gif.py
3 The script will:
  - Determine the smallest Geotiff in the input folder
  - Crop all images to match it's dimensions
  - Convert each to 8-bit RGB
  - Saves the cropped images to the cropped_images directory
  - Generates a GIF of the timeseries with the cropped images
