from flask import Flask, request, jsonify, send_from_directory, render_template
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')  # Ensure this matches your HTML file name

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)
    return 'File uploaded successfully', 200

@app.route('/files', methods=['GET'])
def list_files():
    files = [{'name': f, 'id': f} for f in os.listdir(UPLOAD_FOLDER)]
    return jsonify(files)

# @app.route('/files/<filename>', methods=['GET'])
# def get_file(filename):
#     return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/files/<filename>', methods=['GET'])
def get_file(filename):
    try:
        return send_from_directory(UPLOAD_FOLDER, filename)
    except FileNotFoundError:
        return 'File not found', 404

if __name__ == '__main__':
    app.run(debug=True)
