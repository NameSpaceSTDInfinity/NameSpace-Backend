from flask import Flask, request, jsonify
from google.cloud import datastore
import os
import json
from PyPDF2 import PdfReader
import docx

app = Flask(__name__)

# Initialize the Datastore client
datastore_client = datastore.Client()

# Function to detect file type
def detect_file_type(file_path):
    _, file_extension = os.path.splitext(file_path)
    return file_extension.lower()

# Function to convert PDF to JSON
def pdf_to_json(file_path):
    reader = PdfReader(file_path)
    pages = [page.extract_text() for page in reader.pages]
    return json.dumps({"pages": pages})

# Function to convert DOCX to JSON
def docx_to_json(file_path):
    doc = docx.Document(file_path)
    paragraphs = [para.text for para in doc.paragraphs]
    return json.dumps({"paragraphs": paragraphs})

# Function to convert TXT to JSON
def txt_to_json(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
    return json.dumps({"lines": lines})

# Function to upload the converted JSON data to Google Cloud Datastore
def upload_to_datastore(document_json, user_id, file_type):
    key = datastore_client.key('Document', user_id)
    entity = datastore.Entity(key=key)

    # Add fields to the entity
    entity.update({
        'user_id': user_id,
        'file_type': file_type,
        'document': document_json,
    })

    # Save the entity to Datastore
    datastore_client.put(entity)
    print(f"Document uploaded to Datastore for user {user_id}")

# API route for uploading and processing documents
@app.route('/upload-document', methods=['POST'])
def upload_document():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    user_id = request.form['user_id']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Save the file temporarily
    file_path = os.path.join("/tmp", file.filename)
    file.save(file_path)

    try:
        # Detect file type
        file_type = detect_file_type(file_path)

        # Convert the file to JSON based on its type
        if file_type == '.pdf':
            document_json = pdf_to_json(file_path)
        elif file_type == '.docx':
            document_json = docx_to_json(file_path)
        elif file_type == '.txt':
            document_json = txt_to_json(file_path)
        else:
            return jsonify({"error": "Unsupported file type"}), 400

        # Upload the JSON data directly to Datastore
        upload_to_datastore(document_json, user_id, file_type)

        return jsonify({"message": "Document uploaded successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        # Clean up: Remove the temporary file after processing
        if os.path.exists(file_path):
            os.remove(file_path)

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
