# app.py

from flask import Flask, render_template, request, redirect, url_for
import os
from vehicle import process_video

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['video']

        input_path = os.path.join(UPLOAD_FOLDER, file.filename)
        output_path = os.path.join(OUTPUT_FOLDER, "output.mp4")

        file.save(input_path)

        process_video(input_path, output_path)

        return redirect(url_for('result'))

    return render_template('index.html')

@app.route('/result')
def result():
    return """
    <h2>Processing Done</h2>
    <video width="600" controls>
        <source src="/outputs/output.mp4" type="video/mp4">
    </video>
    """

@app.route('/outputs/<filename>')
def send_file(filename):
    return app.send_static_file(os.path.join('outputs', filename))

if __name__ == '__main__':
    app.run(debug=True)