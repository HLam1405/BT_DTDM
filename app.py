from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import sqlite3, random, os

app=Flask(__name__)
CORS(app)
DB='data.db'
if not os.path.exists(DB):
    conn=sqlite3.connect(DB)
    conn.execute("CREATE TABLE Greetings(id INTEGER PRIMARY KEY AUTOINCREMENT, message TEXT, created_at DATETIME DEFAULT CURRENT_TIMESTAMP)")
    conn.commit()
    conn.close()

def query(q, params=()):
    conn=sqlite3.connect(DB)
    cur=conn.cursor()
    cur.execute(q, params)
    rows=cur.fetchall()
    conn.commit()
    conn.close()
    return rows

@app.route('/')
def ui():
    return send_file('index.html')

@app.route('/api/add', methods=['POST'])
def add():
    j=request.get_json() or {}
    msg=j.get('message')
    if not msg: return jsonify({'error':'no message'}),400
    query("INSERT INTO Greetings(message) VALUES(?)",(msg,))
    return jsonify({'success':True})

@app.route('/api/random')
def random_msg():
    rows=query("SELECT message FROM Greetings")
    if not rows: return jsonify({'error':'empty'}),404
    return jsonify({'message':random.choice(rows)[0]})

@app.route('/api/clear', methods=['DELETE'])
def clear():
    query("DELETE FROM Greetings")
    return jsonify({'success':True})

if __name__=='__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT',5000)))
