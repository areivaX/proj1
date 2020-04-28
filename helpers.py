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
