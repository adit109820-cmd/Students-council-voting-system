from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

DATABASE = "voting.db"

def create_table():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS voting(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        HeadBoy TEXT,
        HeadGirl TEXT,
        SportsCaptain TEXT,
        SportsViceCaptain TEXT,
        GreenHouse TEXT,
        YellowHouse TEXT,
        BlueHouse TEXT,
        RedHouse TEXT
    )
    """)

    conn.commit()
    print("Vote Saved Successfully")
    conn.close()
create_table()    
def save_vote(headboy, headgirl, sports, sportsvice, green, yellow, blue, red):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO voting
    (HeadBoy, HeadGirl, SportsCaptain, SportsViceCaptain, GreenHouse, YellowHouse, BlueHouse, RedHouse)
    VALUES (?,?,?,?,?,?,?,?)
    """,(headboy, headgirl, sports, sportsvice, green, yellow, blue, red))

    conn.commit()
    conn.close()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/vote", methods=["POST"])
def vote():

    headboy = request.form.get("headboy")
    headgirl = request.form.get("headgirl")
    sports = request.form.get("sports")
    sportsvice = request.form.get("sportsvice")
    green = request.form.get("green")
    yellow = request.form.get("yellow")
    blue = request.form.get("blue")
    red = request.form.get("red")
    
    save_vote(headboy, headgirl, sports, sportsvice, green, yellow, blue, red)

    return """
    <h2 align='center'>✅ Your vote has been submitted successfully.</h2>
    <center><a href='/'>Go Back</a></center>
    """
def get_results():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    posts = {
        "Head Boy": "HeadBoy",
        "Head Girl": "HeadGirl",
        "Sports Captain": "SportsCaptain",
        "Sports Vice Captain": "SportsViceCaptain",
        "Green House": "GreenHouse",
        "Yellow House": "YellowHouse",
        "Blue House": "BlueHouse",
        "Red House": "RedHouse"
    }

    results = {}

    for post, column in posts.items():
        cursor.execute(f"""
        SELECT {column}, COUNT(*)
        FROM voting
        GROUP BY {column}
        """)
        results[post] = cursor.fetchall()

    conn.close()
    print(results)
    return results
@app.route("/results")
def results():
    data = get_results()
    return render_template("results.html", results=data)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
