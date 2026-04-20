from flask import Flask, render_template, request, Response
import sqlite3
import psycopg2
import os

def init_db():
    conn = psycopg2.connect(
        dbname="friends-db",
        user="amanbabal",
        password="vEzW5PktZbxqGsEClpSMB1vnNRw58e8t",
        host="dpg-d7ir9on7f7vs739d1ci0-a",
        port="5432"
    )
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

        conn = psycopg2.connect(
            dbname="friends-db",
            user="amanbabal",
            password="vEzW5PktZbxqGsEClpSMB1vnNRw58e8t",
            host="dpg-d7ir9on7f7vs739d1ci0-a",
            port="5432"
            )
        cur = conn.cursor()

        cur.execute("INSERT INTO users VALUES (%s, %s)",(name, review))
        conn.commit()

        conn.close()

    return render_template("index.html")

@app.route("/data")
def data():
    conn = psycopg2.connect(
        dbname="friends-db",
        user="amanbabal",
        password="vEzW5PktZbxqGsEClpSMB1vnNRw58e8t",
        host="dpg-d7ir9on7f7vs739d1ci0-a",
        port="5432"
        )
    cur = conn.cursor()
    cur.execute("SELECT * FROM users")
    rows = cur.fetchall()
    conn.close()

    return render_template("data.html", rows=rows)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)

