import requests

def validate_user(a,b, db):
    user = db.execute("SELECT * FROM users WHERE username = :username AND password = :password",
                {"username":a, "password":b}).fetchone()
    return user


def validate_NewUser(username, pass1, pass2, email, db):
    # make sure there's nobody w same email or same uname in the database
    # make sure passwords match
    # would be good to automatically check username availability without
    # having to submit everything else
    # would also be good to only allow valid emails
    message = ""
    user = None
    if db.execute("SELECT * FROM users WHERE username = :uname", {"uname": username}).rowcount != 0:
        message = "username already taken"
    elif db.execute("SELECT * FROM users WHERE email = :email", {"email": email}).rowcount != 0:
        message = f"there's already an account with email {email}"
    elif pass1 != pass2 : #very naive way to do this, I assume I'll learn a better way later
        message = "the passwords entered do not correspond"
    else:
         db.execute("INSERT INTO users (username, password, email) VALUES (:username, :password, :email)",
            { "username": username, "password":pass1, "email":email }   )
         db.commit()
         user = db.execute("SELECT * FROM users WHERE username = :username AND password = :password",
                     {"username":username, "password":pass1}).fetchone()
    return user, message


def searchBooks(search_type,input, db):

    #res = db.execute("SELECT * FROM books JOIN authors ON books.author_id = authors.id " \
    #                    "WHERE :field LIKE :input", {"input":f"%{input}%", "field":search_type}).fetchall()
    res = db.execute("SELECT * FROM books JOIN authors ON books.author_id = authors.id " \
                    "WHERE "+search_type+" LIKE :name", {"name":'%'+input+'%'}).fetchall()

    #not great that I'm pasting directly to an SQL command? but search_type can only be predetermined values
    return res


def getGRdata(string, key, isbn):
    res = requests.get(string, params={"key": key, "isbns": isbn})
    if res.status_code != 200:
      raise Exception("ERROR: API request unsuccessful.")
    review_data = res.json()
    return review_data


def addReview(uid, rating, text, book_id, db):
    message = ""
    db.execute("INSERT INTO reviews (book_id, user_id, rating, text) VALUES " \
                "(:book_id, :user_id, :rating, :text)",
                {"book_id":book_id, "rating":rating, "text":text, "user_id":uid })
    db.commit()

    return message

def findReview(bID, uID, db):
    rev = db.execute("SELECT * FROM reviews WHERE book_id = :bID AND user_id = :uID",
                {"bID":bID, "uID":uID}).fetchone()
    return rev

def findReviews(bID, db):
    rev = db.execute("SELECT * FROM reviews WHERE book_id = :bID",
            {"bID":bID}).fetchall()
    return rev




def getDict(isbn, db, GRlink, key):
    book = db.execute("SELECT * FROM books JOIN authors ON books.author_id = authors.id " \
                    "WHERE isbn = :isbn", {"isbn":isbn}).fetchone()
    if book is None:
        return 404

    review_data = getGRdata(GRlink,key,isbn)
    rCount = review_data['books'][0]['work_ratings_count'] #i think goodread's json is in incorrect format? selecting from list shouldn't be necessary?
    rAvg = review_data['books'][0]['average_rating']

    dicty = {"title": book.title, "author":book.name, "year":book.year, "isbn":isbn, "review_count":rCount, "average_score":float(rAvg)}
    return dicty
