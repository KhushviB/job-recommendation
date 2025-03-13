# import sys
# import os
# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from werkzeug.utils import secure_filename

# # Add the parent directory to the Python path
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# from models.job_recommender import JobRecommender
# from models.resume_analyser import ResumeAnalyzer  # Ensure this matches the class name in resume_analyser.py

# app = Flask(__name__)
# CORS(app)   

# UPLOAD_FOLDER = 'uploads'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# recommender = JobRecommender()
# resume_analyser = ResumeAnalyzer()  # Create an instance of ResumeAnalyser

# @app.route('/upload_resume', methods=['POST'])
# def upload_resume():
#     if 'file' not in request.files:
#         return jsonify({'error': 'No file part'}), 400
#     file = request.files['file']
#     if file.filename == '':
#         return jsonify({'error': 'No selected file'}), 400

#     if file:
#         filename = secure_filename(file.filename)
#         file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#         file.save(file_path)

#         # Analyze the resume
#         resume_data = resume_analyser.analyze_resume(file_path)  # Call the analyze_resume method
#         return jsonify(resume_data)

# @app.route('/recommendations', methods=['POST'])
# def get_recommendations():
#     user_features = request.json
#     num_recommendations = user_features.pop('num_recommendations', 5)
#     recommendations = recommender.get_recommendations(user_features, num_recommendations)
#     return jsonify(recommendations)

# if __name__ == '__main__':
#     if not os.path.exists(UPLOAD_FOLDER):
#         os.makedirs(UPLOAD_FOLDER)
#     app.run(debug=True)


import sys
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import json # Import json library

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.job_recommender import JobRecommender
from models.resume_analyser import ResumeAnalyzer

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

recommender = JobRecommender()
resume_analyser = ResumeAnalyzer()


@app.route('/')
def home():
    return "Hello, Flask!"

@app.route('/api/data', methods=['GET'])
def get_data():
    sample_data = {
        "message": "Hello from Flask",
        "data": [1, 2, 3, 4, 5]
    }
    return jsonify(sample_data)


@app.route('/upload_resume', methods=['POST'])
def upload_resume():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            print(f"Saving file to: {file_path}")  
            file.save(file_path)

            try:  
                resume_data = resume_analyser.analyze_resume(file_path)
                return jsonify(resume_data)
            except Exception as e:
                print(f"Error analyzing resume: {e}")
                return jsonify({'error': 'Error analyzing resume'}), 500

    except Exception as e:
        print(f"Error uploading resume: {e}")
        return jsonify({'error': 'Failed to upload file'}), 500



@app.route('/recommendations', methods=['POST'])
def get_recommendations():
    try:
        user_features = request.get_json() 
        num_recommendations = user_features.pop('num_recommendations', 5)

        try:  # Handle errors in getting recommendations
            recommendations = recommender.get_recommendations(user_features, num_recommendations)
            return jsonify(recommendations)
        except Exception as e:
            print(f"Error getting recommendations: {e}")
            return jsonify({'error': 'Error getting recommendations'}), 500

    except Exception as e:
        print(f"Error processing request: {e}")
        return jsonify({'error': 'Invalid request data'}), 400

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True, host='0.0.0.0', port=5000) 