import os
import logging
from flask import Flask, render_template, jsonify, request
import pyodbc

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

DB_SERVER = os.getenv("DB_SERVER", "")
DB_NAME = os.getenv("DB_NAME", "")
DB_USER = os.getenv("DB_USER", "")
DB_PASS = os.getenv("DB_PASS", "")
DB_DRIVER = os.getenv("DB_DRIVER", "{ODBC Driver 18 for SQL Server}")

def get_conn():
    if not all([DB_SERVER, DB_NAME, DB_USER, DB_PASS]):
        raise RuntimeError("Database configuration is incomplete")
    conn_str = (
        f"DRIVER={DB_DRIVER};"
        f"SERVER={DB_SERVER};"
        f"DATABASE={DB_NAME};"
        f"UID={DB_USER};"
        f"PWD={DB_PASS};"
        "Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
    )
    return pyodbc.connect(conn_str)

@app.route('/api/add', methods=['POST'])
def add():
    payload = request.get_json(silent=True)
    msg = payload.get("message") if payload else None
    if not msg:
        return jsonify({"error": "Thiếu nội dung"}), 400
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("INSERT INTO Greetings (message) VALUES (?)", (msg,))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"success": True}), 201
    except Exception as e:
        app.logger.exception("Insert failed")
        return jsonify({"error": "Internal server error"}), 500

@app.route("/api/random")
def random_hello():
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("SELECT TOP 1 message FROM Greetings ORDER BY NEWID()")
        row = cur.fetchone()
        cur.close()
        conn.close()
        if not row:
            return jsonify({"message": None}), 204
        return jsonify({"message": row[0]}), 200
    except Exception as e:
        app.logger.exception("Fetch failed")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/api/clear', methods=['DELETE'])
def clear():
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("DELETE FROM Greetings")
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"success": True}), 200
    except Exception as e:
        app.logger.exception("Clear failed")
        return jsonify({"error": "Internal server error"}), 500

@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template("500.html"), 500

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
