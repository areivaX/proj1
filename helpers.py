def validate_user(a,b, db):
    user = db.execute("SELECT * FROM users WHERE username = :username AND password = :password",
                {"username":a, "password":b}).fetchone()
    return user 
