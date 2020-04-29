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


@app.route("/", methods=["GET","POST"])
def index():
    error = None
    if request.method == "POST":
        req = request.form
        #hard-coded for testing
        search_type = req.get("search_options")
        input = req.get("search_input")
        results = searchBooks(search_type,input, db)
        return render_template("search.html", data = results)
    return render_template("search.html", message=error)




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
            session['logged_in'] = True
            flash("success")
            return redirect(url_for('index'))
    return render_template("login.html", message = error)


@app.route("/logout", methods=["GET","POST"])
def logout():
    error=None
    [session.pop(key) for key in list(session.keys())]
    flash("logged out")
    return render_template("index.html", message = "not signed in")


@app.route("/signup", methods=["GET","POST"])
def signup():
    error = None
    if request.method == "POST":
        req = request.form
        inputUname, inputPass, inputPass2, inputEmail = req.get("username"), req.get("password"), req.get("password2"), req.get("email")
        user, message = validate_NewUser(inputUname, inputPass, inputPass2, inputEmail, db)

        if user is None:
            error = message
        else:
            session['current_user'] = user
            session['logged_in'] = True
            flash("user created")
            return redirect(url_for('index'))

    return render_template("signup.html", error=error)
