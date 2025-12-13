import datetime
import math
import secrets
import sqlite3

from flask import Flask
from flask import abort, flash, redirect, render_template, request, session
import markupsafe

import config
import meetings
import users

app = Flask(__name__)
app.secret_key = config.secret_key

def forbidden():
    abort(403)

def not_found():
    abort(404)

def require_login():
    if "user_id" not in session:
        forbidden()

def check_csrf():
    if "csrf_token" not in request.form:
        forbidden()
    if request.form["csrf_token"] != session["csrf_token"]:
        forbidden()

@app.template_filter()
def show_lines(content):
    content = str(markupsafe.escape(content))
    content = content.replace("\n", "<br />")
    return markupsafe.Markup(content)

@app.route("/")
@app.route("/<int:page>")
def index(page=1):
    page_size = 10
    meeting_count = meetings.meeting_count()
    page_count = math.ceil(meeting_count / page_size )
    page_count = max(page_count, 1)

    if page < 1:
        return redirect("/1")
    if page > page_count:
        return redirect("/" + str(page_count))

    all_meetings = meetings.get_meetings(page, page_size)
    return render_template("index.html", page=page, page_count=page_count,
                           all_meetings=all_meetings)

@app.route("/user/<int:user_id>")
def show_user(user_id):
    user = users.get_user(user_id)
    if not user:
        not_found()
    user_meetings = users.get_meetings(user_id)
    return render_template("show_user.html", user=user, user_meetings=user_meetings)

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
        not_found()
    classes = meetings.get_classes(meeting_id)
    participants = meetings.get_participants(meeting_id)
    return render_template("show_meeting.html", meeting=meeting,
                           classes=classes, participants=participants)

@app.route("/new_meeting")
def new_meeting():
    require_login()

    classes = meetings.get_all_classes()
    return render_template("new_meeting.html", classes=classes)

@app.route("/create_meeting", methods=["POST"])
def create_meeting():
    require_login()
    check_csrf()

    topic = request.form["topic"]
    if not topic:
        flash("VIRHE: Aihe puuttuu")
        return redirect("/new_meeting")
    if len(topic) > 50:
        flash("VIRHE: Aiheen pituus yli 50 merkkiä")
        return redirect("/new_meeting")
    description = request.form["description"]
    if not description:
        flash("VIRHE: Kuvaus puuttuu")
        return redirect("/new_meeting")
    if len(description) > 1000:
        flash("VIRHE: Kuvauksen pituus yli 1 000 merkkiä")
        return redirect("/new_meeting")
    date = request.form["date"]
    date_int = datetime.datetime(int(date[:4]), int(date[5:7]), int(date[8:]))
    year = date_int.year
    year_now = datetime.datetime.today().year
    if not date:
        flash("VIRHE: Päivämäärä puuttuu")
        return redirect("/new_meeting")
    if date_int < datetime.datetime.today():
        flash("VIRHE: Et voi järjestää tapahtumaa menneisyydessä")
        return redirect("/new_meeting")
    if year > year_now + 3:
        flash(f"VIRHE: Voit suunnitella tapahtumia vain vuoteen {year_now + 3} asti")
        return redirect("/new_meeting")
    start_time = request.form["start_time"]
    if not start_time:
        flash("VIRHE: Aloitusajankohta puuttuu")
        return redirect("/new_meeting")
    end_time = request.form["end_time"]
    if not end_time:
        flash("VIRHE: Lopetusajankohta puuttuu")
        return redirect("/new_meeting")
    if int(start_time[:2]) > int(end_time[:2]):
        flash("VIRHE: Tapaamisen tulee alkaa ennen kuin se loppuu")
        return redirect("/new_meeting")
    if int(start_time[:2]) <= int(end_time[:2]):
        if int(start_time[3:]) > int(end_time[3:]):
            flash("VIRHE: Tapaamisen tulee alkaa ennen kuin se loppuu")
            return redirect("/new_meeting")
    user_id = session["user_id"]

    all_classes = meetings.get_all_classes()

    classes = []
    for entry in request.form.getlist("classes"):
        if entry:
            title, value = entry.split(":")
            if title not in all_classes:
                flash(f"VIRHE: Luokkaa {title} ei löydy")
                return redirect("/new_meeting")
            if value not in all_classes[title]:
                flash(f"VIRHE: Arvoa {value} ei löydy")
                return redirect("/new_meeting")
            classes.append((title, value))

    meetings.add_meeting(topic, description, date,
                         start_time, end_time, user_id, classes)

    return redirect("/")

@app.route("/participate", methods=["POST"])
def participate():
    require_login()
    check_csrf()

    meeting_id = request.form["meeting_id"]
    meeting = meetings.get_meeting(meeting_id)
    if not meeting:
        not_found()
    user_id = session["user_id"]

    meetings.participate(meeting_id, user_id)

    return redirect("/meeting/" + str(meeting_id))

@app.route("/cancel_participation", methods=["POST"])
def cancel_participation():
    require_login()
    check_csrf()

    meeting_id = request.form["meeting_id"]
    meeting = meetings.get_meeting(meeting_id)
    if not meeting:
        not_found()
    user_id = session["user_id"]

    meetings.cancel_participation(user_id)

    return redirect("/meeting/" + str(meeting_id))

@app.route("/edit_meeting/<int:meeting_id>")
def edit_meeting(meeting_id):
    require_login()

    meeting = meetings.get_meeting(meeting_id)
    if not meeting:
        not_found()
    if meeting["user_id"] != session["user_id"]:
        flash("VIRHE: Sinulla ei ole oikeutta muokata tätä tapahtumaa")
        return redirect(f"/edit_meeting/{meeting_id}")

    all_classes = meetings.get_all_classes()
    classes = {}
    for my_class in all_classes:
        classes[my_class] = ""
    for entry in meetings.get_classes(meeting_id):
        classes[entry["title"]] = entry["value"]

    return render_template("edit_meeting.html", meeting=meeting,
                           classes=classes, all_classes=all_classes)

@app.route("/update_meeting", methods=["POST"])
def update_meeting():
    require_login()
    check_csrf()

    meeting_id = request.form["meeting_id"]
    meeting = meetings.get_meeting(meeting_id)
    if not meeting:
        not_found()
    if meeting["user_id"] != session["user_id"]:
        flash("VIRHE: Sinulla ei ole oikeutta muokata tätä tapahtumaa")
        return redirect(f"/edit_meeting/{meeting_id}")

    topic = request.form["topic"]
    if not topic:
        flash("VIRHE: Aihe puuttuu")
        return redirect(f"/edit_meeting/{meeting_id}")
    if len(topic) > 50:
        flash("VIRHE: Aiheen pituus yli 50 merkkiä")
        return redirect(f"/edit_meeting/{meeting_id}")
    description = request.form["description"]
    if not description:
        flash("VIRHE: Kuvaus puuttuu")
        return redirect(f"/edit_meeting/{meeting_id}")
    if len(description) > 1000:
        flash("VIRHE: Kuvauksen pituus yli 1 000 merkkiä")
        return redirect(f"/edit_meeting/{meeting_id}")
    date = request.form["date"]
    date_int = datetime.datetime(int(date[:4]), int(date[5:7]), int(date[8:]))
    year = date_int.year
    year_now = datetime.datetime.today().year
    if not date:
        flash("VIRHE: Päivämäärä puuttuu")
        return redirect(f"/edit_meeting/{meeting_id}")
    if date_int < datetime.datetime.today():
        flash("VIRHE: Et voi järjestää tapahtumaa menneisyydessä")
        return redirect(f"/edit_meeting/{meeting_id}")
    if year > year_now + 3:
        flash(f"VIRHE: Voit suunnitella tapahtumia vain vuoteen {year_now + 3} asti")
        return redirect(f"/edit_meeting/{meeting_id}")
    start_time = request.form["start_time"]
    if not start_time:
        flash("VIRHE: Aloitusajankohta puuttuu")
        return redirect(f"/edit_meeting/{meeting_id}")
    end_time = request.form["end_time"]
    if not end_time:
        flash("VIRHE: Lopetusajankohta puuttuu")
        return redirect(f"/edit_meeting/{meeting_id}")
    if int(start_time[:2]) > int(end_time[:2]):
        flash("VIRHE: Tapaamisen tulee alkaa ennen kuin se loppuu")
        return redirect(f"/edit_meeting/{meeting_id}")
    if int(start_time[:2]) <= int(end_time[:2]):
        if int(start_time[3:]) > int(end_time[3:]):
            flash("VIRHE: Tapaamisen tulee alkaa ennen kuin se loppuu")
            return redirect(f"/edit_meeting/{meeting_id}")

    all_classes = meetings.get_all_classes()

    classes = []
    for entry in request.form.getlist("classes"):
        if entry:
            title, value = entry.split(":")
            if title not in all_classes:
                flash(f"VIRHE: Luokkaa {title} ei löydy")
                return redirect(f"/edit_meeting/{meeting_id}")
            if value not in all_classes[title]:
                flash(f"VIRHE: Arvoa {value} ei löydy")
                return redirect(f"/edit_meeting/{meeting_id}")
            classes.append((title, value))

    meetings.update_meeting(meeting_id, topic, description,
    date, start_time, end_time, classes)

    return redirect("/meeting/" + str(meeting_id))

@app.route("/remove_meeting/<int:meeting_id>", methods=["GET", "POST"])
def remove_meeting(meeting_id):
    require_login()

    meeting = meetings.get_meeting(meeting_id)
    if not meeting:
        not_found()
    if meeting["user_id"] != session["user_id"]:
        flash("VIRHE: Sinulla ei ole oikeutta poistaa tätä tapahtumaa")
        return redirect(f"/remove_meeting/{meeting_id}")

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
        flash("VIRHE: salasanat eivät ole samat")
        return redirect("/register")

    try:
        users.create_user(username, password1)
    except sqlite3.IntegrityError:
        flash("VIRHE: tunnus on jo varattu")
        return redirect("/register")

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
            session["csrf_token"] = secrets.token_hex(16)
            return redirect("/")
        else:
            flash("VIRHE: väärä tunnus tai salasana")
            return redirect("/login")

@app.route("/logout")
def logout():
    if "user_id" in session:
        del session["user_id"]
        del session["username"]
    return redirect("/")
