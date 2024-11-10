import os
import zipfile
from PIL import Image
import gzip
import bz2
import shutil
import matplotlib.pyplot as plt
from io import BytesIO

# Function to compress text file using gzip (more efficient compression for text files)
def compress_text(file_path):
    compressed_file_path = file_path + ".gz"  # Using gzip for better compression
    with open(file_path, 'rb') as f_in:
        with gzip.open(compressed_file_path, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    return compressed_file_path

# Function to compress image file by reducing both quality and resolution
def compress_image(file_path):
    image = Image.open(file_path)
    
    # Reduce the resolution to 50% for better compression
    width, height = image.size
    image = image.resize((width // 2, height // 2))

    compressed_file_path = file_path.replace(".", "_compressed.")
    image.save(compressed_file_path, optimize=True, quality=30)  # Compress by 30%
    return compressed_file_path

# Function to generate the compression visualization chart
def generate_compression_visualization(original_file_path, compressed_file_path):
    original_size = os.path.getsize(original_file_path)
    compressed_size = os.path.getsize(compressed_file_path)

    # Create a bar chart for the file size comparison
    plt.bar(['Original', 'Compressed'], [original_size, compressed_size], color=['blue', 'green'])
    plt.ylabel('File Size (Bytes)')
    plt.title('Compression Effect')

    # Save the plot to the static folder as a PNG file
    static_folder = 'static'
    img_path = os.path.join(static_folder, 'compression_chart.png')
    plt.savefig(img_path)
    plt.close()  # Close the plot to free up memory

    return img_path
