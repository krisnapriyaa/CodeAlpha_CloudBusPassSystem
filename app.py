from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    
    c.execute('''
    CREATE TABLE IF NOT EXISTS tickets(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        source TEXT,
        destination TEXT,
        price INTEGER
    )
    ''')
    
    conn.commit()
    conn.close()

init_db()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/book", methods=["GET","POST"])
def book():
    
    if request.method == "POST":
        
        name = request.form["name"]
        source = request.form["source"]
        destination = request.form["destination"]
        
        price = 50   # fixed pricing
        
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        
        c.execute("INSERT INTO tickets(name,source,destination,price) VALUES(?,?,?,?)",
                  (name,source,destination,price))
        
        conn.commit()
        conn.close()
        
        return "Ticket Booked Successfully!"
        
    return render_template("book.html")

@app.route("/tickets")
def tickets():
    
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    
    c.execute("SELECT * FROM tickets")
    
    data = c.fetchall()
    
    conn.close()
    
    return render_template("tickets.html",data=data)

if __name__ == "__main__":
    app.run(debug=True)