from flask import Flask, render_template, request, Response
import sqlite3
import psycopg2
import os

DATABASE_URL = os.environ.get("postgresql://amanbabal:vEzW5PktZbxqGsEClpSMB1vnNRw58e8t@dpg-d7ir9on7f7vs739d1ci0-a/friendsdb_v60c")

def check_auth(username, password):
    return username == "admin" and password == "1234"

def authenticate():
    return Response(
        "Login required", 401,
        {"WWW-Authenticate": 'Basic realm="Login Required"'}
    )

def init_db():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            name TEXT,
            review TEXT
        )
    """)
    conn.commit()
    conn.close()

app = Flask(__name__)
init_db()

@app.route("/", methods = ["GET", "POST"])
def home():
    if request.method == "POST":
        name = request.form["name"]
        review = request.form["review"]

        conn = psycopg2.connect(DATABASE_URL)

        cur = conn.cursor()

        cur.execute(
            "INSERT INTO users (name, review) VALUES (%s, %s)",
            (name, review)
            )
        conn.commit()

        conn.close()

    return render_template("index.html")

@app.route("/data")
def data():
    auth = request.authorization
    if not auth or not check_auth(auth.username, auth.password):
        return authenticate()
    
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute("SELECT * FROM users")
    rows = cur.fetchall()
    conn.close()
    return render_template("data.html", rows=rows)
    print(name, review)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5432)

