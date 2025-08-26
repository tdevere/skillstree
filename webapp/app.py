from flask import Flask, jsonify, request, render_template, send_from_directory
import os
import json
from pathlib import Path

app = Flask(__name__, static_folder='static', template_folder='templates')

def get_repo_root():
    return Path(__file__).resolve().parents[1]

def get_data_dir():
    # Prefer explicit env var, else use platform-appropriate local app data or home
    env = os.environ.get('SKILLSTREE_DATA_DIR')
    if env:
        p = Path(env)
    else:
        if os.name == 'nt':
            base = Path(os.environ.get('LOCALAPPDATA') or os.environ.get('APPDATA') or Path.home())
        else:
            base = Path.home()
        p = base / '.skillstree'
    p.mkdir(parents=True, exist_ok=True)
    return p

def get_progress_file():
    return get_data_dir() / 'progress.json'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/skill_tree')
def api_skill_tree():
    repo_root = get_repo_root()
    st = repo_root / 'skill_tree.json'
    if not st.exists():
        return jsonify({'error': 'skill_tree.json not found'}), 404
    with st.open('r', encoding='utf-8') as f:
        data = json.load(f)
    return jsonify(data)

@app.route('/api/progress', methods=['GET', 'POST'])
def api_progress():
    pf = get_progress_file()
    if request.method == 'GET':
        if not pf.exists():
            return jsonify({})
        with pf.open('r', encoding='utf-8') as f:
            return jsonify(json.load(f))
    else:
        body = request.get_json(force=True)
        # Basic validation: must be a dict
        if not isinstance(body, dict):
            return jsonify({'error': 'progress must be an object'}), 400
        with pf.open('w', encoding='utf-8') as f:
            json.dump(body, f, indent=2)
        return jsonify({'status': 'saved'})

@app.route('/static/<path:p>')
def static_files(p):
    return send_from_directory(app.static_folder, p)

if __name__ == '__main__':
    port = int(os.environ.get('SKILLSTREE_PORT', '5000'))
    app.run(host='127.0.0.1', port=port)
