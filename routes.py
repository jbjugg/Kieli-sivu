from app import app
from flask import render_template, redirect, request, session
from sqlalchemy import text
from db import db
import users, languages, exercises, results, comments

@app.route("/", methods=["GET"])
def front():
    sql = text("""
        SELECT languages.id, languages.language, COUNT(exercises.id) AS exercise_count
        FROM languages
        LEFT JOIN exercises ON languages.id = exercises.language_id
        GROUP BY languages.id
        ORDER BY languages.language
    """)
    result = db.session.execute(sql)
    languages = result.fetchall()
    return render_template("front.html", languages=languages)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = users.login(username, password)

        if user:
            return redirect("/")
        else:
            return render_template("error.html", message="Väärä tunnus tai salasana")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if len(username) > 50:
            return render_template("error.html", message="Et sä noin pitkää nimee tarvii")
        if password1 != password2:
            return render_template("error.html", message="Noihan on eri salasanat")
        if users.register(username, password1):
            return redirect("/")
        else:
            return render_template("error.html", message="Rekisteröinti ei onnistunut")
