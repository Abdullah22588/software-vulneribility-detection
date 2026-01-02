
import os
import sys
from flask import Flask, render_template, request, jsonify, send_from_directory, url_for
from werkzeug.utils import secure_filename

# Ensure we can import from local modules
sys.path.append(os.getcwd())

from analyzer.ast_detector import analyze_file
from visualizer.automata_visualizer import draw_pattern
from automata.pattern_definitions import PATTERN_LIST_FOR_VIS

app = Flask(__name__, template_folder='web_app/templates', static_folder='web_app/static')

UPLOAD_FOLDER = 'web_app/uploads'
RESULTS_FOLDER = 'web_app/results'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULTS_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULTS_FOLDER'] = RESULTS_FOLDER

def generate_visuals():
    """Generates the static automata diagrams if they don't exist."""
    vis_images = []
    try:
        for name, defn in PATTERN_LIST_FOR_VIS.items():
            filename = f"{name.replace(' ', '_')}.gv.png"
            output_path = os.path.join(RESULTS_FOLDER, filename)
            
            # Draw regardless to ensure fresh style or existence
            draw_pattern(name, defn['states'], defn['transitions'], 
                         defn['start'], defn['accept'], output_dir=RESULTS_FOLDER)
            
            vis_images.append({'name': name, 'filename': filename})
    except Exception as e:
        print(f"Error generating visuals: {e}")
    return vis_images

# Generate visuals on startup
VISUAL_ASSETS = generate_visuals()

@app.route('/')
def index():
    return render_template('index.html', visuals=VISUAL_ASSETS)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Run Analysis
        try:
            results = analyze_file(filepath)
            # Parse results to separate vulnerabilities from safe messages
            parsed_results = {
                'vulnerabilities': [r for r in results if "Vulnerability Detected" in r],
                'safe': [r for r in results if "No known vulnerabilities" in r],
                'errors': [r for r in results if "Could not parse" in r],
                'raw': results
            }
            return jsonify({'success': True, 'results': parsed_results})
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/results/<path:filename>')
def serve_result(filename):
    return send_from_directory(app.config['RESULTS_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
