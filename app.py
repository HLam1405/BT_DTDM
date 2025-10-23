from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)  

messages = []

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/add', methods=['POST'])
def add_message():
    data = request.get_json()
    msg = data.get('message', '').strip()
    if msg:
        messages.append(msg)
        return jsonify({"status": "ok"}), 200
    return jsonify({"status": "error", "message": "No message provided"}), 400

@app.route('/api/random', methods=['GET'])
def random_message():
    if not messages:
        return jsonify({"status": "error", "message": ""}), 200
    msg = random.choice(messages)
    return jsonify({"status": "ok", "message": msg}), 200

@app.route('/api/clear', methods=['DELETE'])
def clear_messages():
    messages.clear()
    return jsonify({"status": "ok"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
