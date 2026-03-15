from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Create database
def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS tickets(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        source TEXT,
        destination TEXT,
        time TEXT,
        seat TEXT,
        price INTEGER
    )
    """)

    conn.commit()
    conn.close()

init_db()


# Home page
@app.route("/")
def index():
    return render_template("index.html")


# Book ticket
@app.route("/book", methods=["GET","POST"])
def book():

    if request.method == "POST":

        name = request.form["name"]
        source = request.form["source"]
        destination = request.form["destination"]
        time = request.form["time"]
        seat = request.form["seat"]

        price = 50

        conn = sqlite3.connect("database.db")
        c = conn.cursor()

        c.execute("INSERT INTO tickets (name,source,destination,time,seat,price) VALUES (?,?,?,?,?,?)",
                  (name,source,destination,time,seat,price))

        conn.commit()
        conn.close()

        return redirect("/tickets")

    return render_template("book.html")


# View tickets
@app.route("/tickets")
def tickets():

    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("SELECT * FROM tickets")
    data = c.fetchall()

    conn.close()

    return render_template("tickets.html", data=data)


# Cancel ticket
@app.route("/cancel/<int:id>")
def cancel(id):

    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("DELETE FROM tickets WHERE id=?", (id,))

    conn.commit()
    conn.close()

    return redirect("/tickets")


if __name__ == "__main__":
    app.run(debug=True)