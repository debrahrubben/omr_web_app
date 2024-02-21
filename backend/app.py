from flask import Flask, request, jsonify
from flask_cors import CORS
from io import BytesIO
import pytesseract
from PIL import Image

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/', methods=['POST'])
def process_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    image_file = request.files['image']
    if image_file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        extracted_text = ocr(image_file)
        marked_answers = process_text(extracted_text)
        return jsonify(marked_answers)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def ocr(image_file):
    # Use pytesseract directly on the uploaded image file
    extracted_text = pytesseract.image_to_string(Image.open(BytesIO(image_file.read())))
    return extracted_text

def process_text(extracted_text):
    lines = extracted_text.split('\n')
    marked_answers = []

    for line in lines:
        if line.strip():
            question_number = line[:2]
            marked_answer = line[-3]
            marked_answers.append({'questionNumber': question_number, 'markedAnswer': marked_answer})

    return marked_answers

if __name__ == '__main__':
    app.run(debug=True)
