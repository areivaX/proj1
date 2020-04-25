import os
from helpers import *
from flask import Flask, session, request, render_template, flash, redirect, url_for
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    if 'username' in session:
        return render_template("index.html", message = "logged in as " + session['current_user'].username)
    return render_template("index.html", message="not signed in")



@app.route("/login", methods=["GET","POST"])
def login():
    error=None
    if request.method == "POST":
        req = request.form
        inputUname, inputPass = req.get("username"), req.get("password")
        user = validate_user(inputUname, inputPass, db)
        if user is None:
            error = "incorrect username or password"
        else:
            session['current_user'] = user
            flash("success")
            return redirect(url_for('index'))
    return render_template("login.html", error=error)
