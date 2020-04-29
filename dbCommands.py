import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


def a1():
    db.execute("CREATE TABLE authors (author_id SERIAL PRIMARY KEY, name VARCHAR NOT NULL) ")
    db.commit()

def a10():
    db.execute("ALTER TABLE authors RENAME COLUMN author_id TO id")
    db.commit()


def a2():
    db.execute("CREATE TABLE books " \
                    "(isbn INTEGER PRIMARY KEY, "\
                    "title VARCHAR, "\
                    "author_id INTEGER REFERENCES authors )")
    db.commit()


def a3():
    db.execute("ALTER TABLE authors ADD CONSTRAINT a_name unique(name)")
    db.commit()



def a4():
    db.execute("ALTER TABLE books ADD year INTEGER")
    db.commit()

def a5():
    db.execute("ALTER TABLE books ALTER COLUMN isbn TYPE VARCHAR")
    db.commit()


def a6():
    res = db.execute("SELECT * FROM books JOIN authors ON books.author_id = authors.id ").fetchone()
    print(res)
a6()
