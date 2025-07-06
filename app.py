# Codsoft Bot Project
# Author: Kunal Arya
# Version: Flask Edition v1.0

from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import os
import base64
from caption_generator import generate_caption
from recommender import recommend
from face_recog import detect_face

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chatbot', methods=['GET', 'POST'])
def chatbot_page():
    response = ""
    if request.method == 'POST':
        user_input = request.form['user_input']
        if "hello" in user_input.lower():
            response = "Hello! How can I assist you?"
        elif "name" in user_input.lower():
            response = "I'm Codsoft Bot, your AI assistant."
        elif "bye" in user_input.lower():
            response = "Goodbye! Come back soon."
        else:
            response = "I'm still learning to respond to that."
    return render_template('chatbot.html', response=response)

@app.route('/tictactoe')
def tictactoe_page():
    return render_template('tictactoe.html')

@app.route('/caption', methods=['GET', 'POST'])
def caption_page():
    if request.method == 'POST':
        style = request.form.get('style', 'default')

        if 'image_file' in request.form:
            image_file = request.form['image_file']
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_file)
            caption = generate_caption(image_path, style)
            return render_template('caption_result.html', caption=caption, image_file=image_file, style=style)

        file = request.files.get('image')
        if file and file.filename != '':
            image_file = secure_filename(file.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_file)
            file.save(image_path)
            caption = generate_caption(image_path, style)
            return render_template('caption_result.html', caption=caption, image_file=image_file, style=style)

        return render_template('caption.html', error="No image provided.")
    return render_template('caption.html')

@app.route('/recommend', methods=['GET', 'POST'])
def recommend_page():
    recommendations = []
    if request.method == 'POST':
        query = request.form.get('query')
        category = request.form.get('category')
        min_rating = request.form.get('min_rating', 0)

        try:
            min_rating = float(min_rating)
        except:
            min_rating = 0

        recommendations = recommend(query, category=category, min_rating=min_rating)
    return render_template('recommend.html', recommendations=recommendations)

@app.route('/face', methods=['GET', 'POST'])
def face_page():
    face_result = ""
    recognition_result = ""
    output_path = None

    if request.method == 'POST':
        if 'captured' in request.form and request.form['captured']:
            data_url = request.form['captured']
            header, encoded = data_url.split(",")
            binary_data = base64.b64decode(encoded)
            filename = os.path.join(app.config['UPLOAD_FOLDER'], 'captured_image.png')
            with open(filename, "wb") as f:
                f.write(binary_data)
            face_result, output_path = detect_face(filename)
            recognition_result = ""

        elif 'media' in request.files:
            file = request.files['media']
            if file and file.filename != '':
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                face_result, output_path = detect_face(file_path)
                recognition_result = ""

    return render_template('face.html',
        face_result=face_result,
        recognition_result=recognition_result,
        face_image=output_path
    )

if __name__ == '__main__':
    app.run(debug=True, port=5500)
