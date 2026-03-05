from flask import Flask, render_template, request, jsonify
import pymysql
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

def get_db():
    return pymysql.connect(
        host        = os.getenv("DB_HOST"),
        port        = int(os.getenv("DB_PORT")),
        database    = os.getenv("DB_NAME"),
        user        = os.getenv("DB_USER"),
        password    = os.getenv("DB_PASSWORD"),
        cursorclass = pymysql.cursors.DictCursor
    )

def init_db():
    conn = get_db()
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id      INT AUTO_INCREMENT PRIMARY KEY,
                name    VARCHAR(100) NOT NULL,
                email   VARCHAR(100) UNIQUE NOT NULL,
                created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
    conn.commit()
    conn.close()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/health")
def health():
    return jsonify({"status": "healthy", "version": "1.0.0"}), 200

@app.route("/users", methods=["GET"])
def get_users():
    conn = get_db()
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM users ORDER BY id DESC")
        users = cur.fetchall()
    conn.close()
    return jsonify(users), 200

@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    if not data or not data.get("name") or not data.get("email"):
        return jsonify({"error": "name and email are required"}), 400
    conn = get_db()
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO users (name, email) VALUES (%s, %s)",
            (data["name"], data["email"])
        )
    conn.commit()
    conn.close()
    return jsonify({"message": "User created successfully!"}), 201

@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    conn = get_db()
    with conn.cursor() as cur:
        cur.execute("DELETE FROM users WHERE id = %s", (user_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": f"User {user_id} deleted"}), 200

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)
