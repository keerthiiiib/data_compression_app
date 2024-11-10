from flask import Flask, request, render_template, send_from_directory
import os
from compression import compress_text, compress_image, generate_compression_visualization

app = Flask(__name__)

# Set up the folder paths
UPLOAD_FOLDER = 'uploads'
COMPRESSED_FOLDER = 'compressed_files'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['COMPRESSED_FOLDER'] = COMPRESSED_FOLDER

# Ensure the directories exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
if not os.path.exists(COMPRESSED_FOLDER):
    os.makedirs(COMPRESSED_FOLDER)

# Route for the home page
@app.route('/')
def index():
    return render_template('index.html')

# Route for handling file compression
@app.route('/compress', methods=['POST'])
def compress():
    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400
    
    # Save the uploaded file
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)
    
    # Compress the file (text or image)
    if file.filename.endswith('.txt'):
        compressed_file_path = compress_text(file_path)
    elif file.filename.endswith(('.png', '.jpg', '.jpeg')):
        compressed_file_path = compress_image(file_path)
    else:
        return 'Unsupported file type', 400

    # Generate the compression visualization and save it in the static folder
    chart_img_path = generate_compression_visualization(file_path, compressed_file_path)

    # Move the compressed file to the 'compressed_files' folder for easy access
    compressed_filename = os.path.basename(compressed_file_path)
    new_compressed_file_path = os.path.join(COMPRESSED_FOLDER, compressed_filename)
    os.rename(compressed_file_path, new_compressed_file_path)

    return render_template('index.html', 
                           chart_img_path=chart_img_path, 
                           compressed_file_path=compressed_filename)

# Route for downloading compressed files
@app.route('/download/<filename>')
def download_file(filename):
    # Securely join the filename with the folder path
    try:
        return send_from_directory(app.config['COMPRESSED_FOLDER'], filename, as_attachment=True)
    except FileNotFoundError:
        return "File not found", 404

if __name__ == '__main__':
    app.run(debug=True)
