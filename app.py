from flask import Flask, render_template, request
import sqlite3


def init_db():
    conn = sqlite3.connect("data.db")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            name TEXT,
            review TEXT
        )
    """)

app = Flask(__name__)
init_db()

@app.route("/", methods = ["GET", "POST"])
def home():
    if request.method == "POST":
        name = request.form["name"]
        review = request.form["review"]

        conn = sqlite3.connect("data.db")

        conn.execute("Insert into users values (?, ?)", (name, review))

        conn.commit()

        conn.close()

    return render_template("index.html")

@app.route("/data")
def data():
    conn = sqlite3.connect("data.db")
    cursor = conn.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    conn.close()
    return render_template("data.html", rows=rows)
    print(name, review)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

