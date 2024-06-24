
import os
from flask import Flask, request, render_template, send_file, jsonify
import subprocess

app = Flask(__name__)
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
OUTPUT_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output')

for folder in [UPLOAD_FOLDER, OUTPUT_FOLDER]:
    if not os.path.exists(folder):
        os.makedirs(folder)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file:
        filename = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filename)
        return jsonify({'filename': file.filename}), 200

@app.route('/cut', methods=['POST'])
def cut_video():
    data = request.json
    input_file = os.path.join(UPLOAD_FOLDER, data['input_file'])
    segments = data['segments']
    output_file = os.path.join(OUTPUT_FOLDER, f"cut_{os.path.basename(input_file)}")
    
    if not os.path.exists(input_file):
        return jsonify({'error': 'Input file not found'}), 400
    
    # Create a temporary file to store the complex filter
    filter_file = os.path.join(OUTPUT_FOLDER, "filter.txt")
    with open(filter_file, 'w') as f:
        for i, segment in enumerate(segments):
            f.write(f"[0:v]trim=start={segment['start']}:end={segment['end']},setpts=PTS-STARTPTS[v{i}];\n")
            f.write(f"[0:a]atrim=start={segment['start']}:end={segment['end']},asetpts=PTS-STARTPTS[a{i}];\n")
        
        video_parts = ''.join(f'[v{i}]' for i in range(len(segments)))
        audio_parts = ''.join(f'[a{i}]' for i in range(len(segments)))
        f.write(f"{video_parts}concat=n={len(segments)}:v=1:a=0[outv];\n")
        f.write(f"{audio_parts}concat=n={len(segments)}:v=0:a=1[outa]")

    # FFmpeg command to cut and concatenate multiple segments
    cmd = f"ffmpeg -y -i \"{input_file}\" -filter_complex_script \"{filter_file}\" -map \"[outv]\" -map \"[outa]\" \"{output_file}\""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    # Clean up the temporary filter file
    os.remove(filter_file)
    
    if result.returncode != 0:
        return jsonify({'error': 'Error cutting video', 'details': result.stderr}), 500
    
    if not os.path.exists(output_file):
        return jsonify({'error': 'Output file not created'}), 500
    
    return send_file(output_file, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
