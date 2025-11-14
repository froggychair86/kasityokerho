import sqlite3
from flask import Flask
from flask import abort, redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
import config
import db
import meetings

app = Flask(__name__)
app.secret_key = config.secret_key

def require_login():
    if "user_id" not in session:
        abort(403)

@app.route("/")
def index():
    all_meetings = meetings.get_meetings()
    return render_template("index.html", meetings=all_meetings)

@app.route("/find_meeting")
def find_meeting():
    query = request.args.get("query")
    if query:
        results = meetings.find_meetings(query)
    else:
        query = ""
        results = []
    return render_template("find_meeting.html", query=query, results=results)

@app.route("/meeting/<int:meeting_id>")
def show_meeting(meeting_id):
    meeting = meetings.get_meeting(meeting_id)
    if not meeting:
        abort(404)
    return render_template("show_meeting.html", meeting=meeting)

@app.route("/new_meeting")
def new_item():
    require_login()
    return render_template("new_meeting.html")

@app.route("/create_meeting", methods=["POST"])
def create_meeting():
    require_login()

    topic = request.form["topic"]
    description = request.form["description"]
    date = request.form["date"]
    start_time = request.form["start_time"]
    end_time = request.form["end_time"]
    user_id = session["user_id"]

    meetings.add_meeting(topic, description, date, start_time, end_time, user_id)

    return redirect("/")

@app.route("/edit_meeting/<int:meeting_id>")
def edit_meeting(meeting_id):
    require_login()
    meeting = meetings.get_meeting(meeting_id)
    if not meeting:
        abort(404)
    if meeting["user_id"] != session["user_id"]:
        abort(403)
    return render_template("edit_meeting.html", meeting=meeting)

@app.route("/update_meeting", methods=["POST"])
def update_meeting():
    require_login()
    meeting_id = request.form["meeting_id"]
    meeting = meetings.get_meeting(meeting_id)
    if not meeting:
        abort(404)
    if meeting["user_id"] != session["user_id"]:
        abort(403)

    topic = request.form["topic"]
    description = request.form["description"]
    date = request.form["date"]
    start_time = request.form["start_time"]
    end_time = request.form["end_time"]

    meetings.update_meeting(meeting_id, topic, description, date, start_time, end_time)

    return redirect("/meeting/" + str(meeting_id))

@app.route("/remove_meeting/<int:meeting_id>", methods=["GET", "POST"])
def remove_meeting(meeting_id):
    require_login()
    meeting = meetings.get_meeting(meeting_id)
    if not meeting:
        abort(404)
    if meeting["user_id"] != session["user_id"]:
        abort(403)

    if request.method == "GET":
        return render_template("remove_meeting.html", meeting=meeting)

    if request.method == "POST":
        if "remove" in request.form:
            meetings.remove_meeting(meeting_id)
            return redirect("/")
        else:
            return redirect("/meeting/" + str(meeting_id))

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        return "VIRHE: salasanat eivät ole samat"
    password_hash = generate_password_hash(password1)

    try:
        sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        db.execute(sql, [username, password_hash])
    except sqlite3.IntegrityError:
        return "VIRHE: tunnus on jo varattu"

    return "Tunnus luotu"

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        sql = "SELECT id, password_hash FROM users WHERE username = ?"
        result = db.query(sql, [username])[0]
        user_id = result["id"]
        password_hash = result["password_hash"]

        if check_password_hash(password_hash, password):
            session["user_id"] = user_id
            session["username"] = username
            return redirect("/")
        else:
            return "VIRHE: väärä tunnus tai salasana"

@app.route("/logout")
def logout():
    if "user_id" in session:
        del session["user_id"]
        del session["username"]
    return redirect("/")