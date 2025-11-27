import sqlite3
from flask import Flask
from flask import abort, redirect, render_template, request, session
from datetime import date
import config
import db
import meetings
import users

app = Flask(__name__)
app.secret_key = config.secret_key

def require_login():
    if "user_id" not in session:
        abort(403)

@app.route("/")
def index():
    all_meetings = meetings.get_meetings()
    return render_template("index.html", meetings=all_meetings)

@app.route("/user/<int:user_id>")
def show_user(user_id):
    user = users.get_user(user_id)
    if not user:
        abort(404)
    meetings = users.get_meetings(user_id)
    return render_template("show_user.html", user=user, meetings=meetings)

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
    classes = meetings.get_classes(meeting_id)
    return render_template("show_meeting.html", meeting=meeting, classes=classes)

@app.route("/new_meeting")
def new_item():
    require_login()
    return render_template("new_meeting.html")

@app.route("/create_meeting", methods=["POST"])
def create_meeting():
    require_login()

    topic = request.form["topic"]
    if not topic or len(topic) > 50:
        abort(403)
    description = request.form["description"]
    if not description or len(description) > 1000:
        abort(403)
    date = request.form["date"]
    if not date:
        abort(403)
    start_time = request.form["start_time"]
    if not start_time:
        abort(403)
    end_time = request.form["end_time"]
    if not end_time:
        abort(403)
    user_id = session["user_id"]

    classes = []
    guidance = request.form["guidance"]
    if guidance:
        classes.append(("Ohjaus", guidance))

    meetings.add_meeting(topic, description, date, start_time, end_time, user_id, classes)

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
    if not topic or len(topic) > 50:
        abort(403)
    description = request.form["description"]
    if not description or len(description) > 1000:
        abort(403)
    date = request.form["date"]
    if not date:
        abort(403)
    start_time = request.form["start_time"]
    if not start_time:
        abort(403)
    end_time = request.form["end_time"]
    if not end_time:
        abort(403)

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

    try:
        users.create_user(username, password1)
    except sqlite3.IntegrityError:
        return "VIRHE: tunnus on jo varattu"

    return render_template("create.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user_id = users.check_login(username, password)
        if user_id:
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