from flask import Flask, render_template, request
import cv2
import numpy as np
import logging

app = Flask(__name__)

# Constants
QUESTION_SPACING = 50
NUM_QUESTIONS = 5

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def process_image(file, correct_answers):
    try:
        # Read the uploaded image
        image = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_GRAYSCALE)

        # With Otsu's thresholding
        _, thresholded = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # Invert the image (optional, depending on your needs)
        thresholded = cv2.bitwise_not(thresholded)

        # Add your OMR logic here
        for question_number in range(1, NUM_QUESTIONS + 1):
            # Get the region of interest (ROI) for the current question
            roi_y = question_number * QUESTION_SPACING
            roi = thresholded[roi_y:roi_y + QUESTION_SPACING, :]

            # Calculate the percentage of white pixels in the ROI
            white_pixel_percentage = np.count_nonzero(roi == 255) / roi.size

            # Set a threshold for considering the answer as shaded
            shading_threshold = 0.5  # Adjust this threshold based on your needs

            # Simulate OMR processing logic by checking if the answer is shaded
            answer_key = 'A' if white_pixel_percentage < shading_threshold else 'Not answered'

            # Retrieve the correct answer from the form
            correct_answer = correct_answers.get(f'q{question_number}')

            # Evaluate the user's answer
            is_correct = answer_key == correct_answer

            logger.info(f"Question {question_number}: {'Shaded' if answer_key == 'A' else 'Not Shaded'}, "
                        f"User's Answer: {correct_answer}, "
                        f"Is Correct: {is_correct}")

        return "File processed successfully"
    except Exception as e:
        logger.error(f"Error processing image: {e}")
        return "Error processing image"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return "No file part"
    file = request.files['file']

    if file.filename == '':
        return "No selected file"
    # Retrieve correct answers from the form
    correct_answers = {key: request.form[key] for key in request.form.keys() if key.startswith('q')}

    result = process_image(file, correct_answers)
    
    return result

if __name__ == '__main__':
    app.run(debug=True)
