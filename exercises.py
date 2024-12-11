from app import app
from flask import render_template, redirect, request, session
from sqlalchemy import text
from db import db

@app.route("/new")
def new():
    result = db.session.execute(text("SELECT L.id, L.language, U.id AS user_id FROM languages L, users U ORDER BY language"))
    languages = result.fetchall()
    user_id = 1
    return render_template("new.html", languages=languages, user_id=user_id)

@app.route("/create", methods=["POST"])
def create():
    topic = request.form.get("topic")
    exercise = request.form.get("exercise")
    deadline = request.form.get("deadline")
    language_id = request.form.get("language_id")
    user_id = request.form.get("user_id")
    
    if not topic:
        return "Topic cannot be empty", 400
    try:
        sql = text("INSERT INTO exercises (topic, exercise, deadline, language_id, user_id) VALUES (:topic, :exercise, :deadline, :language_id, :user_id) RETURNING id")  
        db.session.execute(sql, {"topic": topic, "exercise" :exercise, "deadline" :deadline, "language_id" :language_id, "user_id" :user_id})
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print("Error creating exercise:", e)
        return "An error occurred while creating the exercise.", 500
    return redirect("/")

@app.route("/exercise/<int:id>")
def exercise(id):  
    result = db.session.execute(text("SELECT id, topic, exercise FROM exercises WHERE id=:id") , {"id": id})
    exercises = result.fetchone()
    result2 = db.session.execute(text("SELECT users.id, users.username FROM users, exercises WHERE users.id = exercises.user_id"))
    users = result2.fetchone()
    return render_template("exercise.html", exercises=exercises, users=users)

@app.route("/answer", methods=["POST"])
def answer():
    answer = request.form.get("answer")
    exercise_id = request.form.get("id")
    user_id = session.get("user_id")
    sql = text("INSERT INTO answers (answer, exercise_id, user_id) VALUES (:answer, :exercise_id, :user_id) RETURNING id")
    db.session.execute(sql, {"answer": answer, "exercise_id": exercise_id, "user_id" :user_id})
    db.session.commit()
    return redirect("/")
