import os
from helpers import *
from flask import Flask, session, request, render_template, flash, redirect, url_for, jsonify, abort
import requests
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

goodReadsRevCount = "https://www.goodreads.com/book/review_counts.json"
goodReadsRev = "https://www.goodreads.com/book/isbn/ISBN?format=FORMAT"
xkey = "lfvEC9SpVfHoOt44qSldow"


@app.errorhandler(404)
def page_not_found(error):
   return render_template('404.html', title = '404'), 404

@app.route("/", methods=["GET","POST"])
def index():
    error = ""
    if request.method == "POST":
        req = request.form
        #hard-coded for testing
        search_type = req.get("search_options")
        input = req.get("search_input")
        input = input.lower()
        results = searchBooks(search_type,input, db)
        if len(results) == 0:
            error = "no book meets your search criteria"
        return render_template("search.html", data = results, message=error)
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
            flash(error)
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
    return render_template("index.html",message="you are logged out")


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


@app.route("/book/<book_id>", methods=["GET","POST"])
def book(book_id):
    error=""
    book = db.execute("SELECT * FROM books JOIN authors ON books.author_id = authors.id " \
                    "WHERE book_id = :id", {"id":int(book_id)}).fetchone()

    if 'logged_in' in list(session.keys()):
        npr = findReview(book_id, session['current_user'].user_id, db) is None
    else:
        npr = "who cares"

    other_reviews = findReviews(book_id,db)

    review_data = getGRdata(goodReadsRevCount,xkey,book.isbn)
    rCount = review_data['books'][0]['work_ratings_count']
    rAvg = review_data['books'][0]['average_rating']


    if request.method == "POST":
        req = request.form
        rating, text = req.get("rating"), req.get("review_text")
        error = addReview(session['current_user'].user_id, rating, text, book_id, db)
        if error=="":
            flash("review submitted")
        return redirect(url_for('book', book_id=book_id))

    return render_template("book.html", book=book, reviews = other_reviews,
                    rCount = rCount, rAvg = rAvg, message=error, no_prev_review=npr)

@app.route("/api/<isbn>")
def api(isbn):
    dicty = getDict(isbn, db, goodReadsRevCount ,xkey)
    if dicty==404:
        abort(404)
    #should return 404 error if isbn not in db
    return jsonify(dicty)
