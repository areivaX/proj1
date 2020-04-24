import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

def main():
    f = open("media/users.csv")
    reader = csv.reader(f)
    for line in reader:
        user, email, passw = line[0], line[1], line[2]
        db.execute("INSERT INTO users (username, email, password) VALUES (:username, :email, :password)",
                   {"username": user, "email": email, "password": passw})
        print(f"Added user {user} to users db.")
    db.commit()

if __name__ == "__main__":
    main()
