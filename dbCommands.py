import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask import Flask, session, request, render_template, flash, redirect, url_for


engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

goodReadsApi = "https://www.goodreads.com/book/"



def a1():
    db.execute("CREATE TABLE authors (author_id SERIAL PRIMARY KEY, name VARCHAR NOT NULL) ")
    db.commit()

def a1_0():
    db.execute("ALTER TABLE authors RENAME COLUMN author_id TO id")
    db.commit()

def a1_1():
    db.execute("CREATE TABLE reviews (review_id SERIAL PRIMARY KEY, book_id INTEGER REFERENCES books, " \
                "user_id INTEGER REFERENCES users, rating INTEGER, " \
                "CONSTRAINT rating_values CHECK (rating>0 AND rating<6) )")
    db.commit()

def a1_2():
    db.execute("ALTER TABLE reviews ADD text VARCHAR")
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

def a5_0():
    db.execute("ALTER TABLE books ADD CONSTRAINT a_isbn unique(isbn)")
    db.commit()


def a6():
    res = db.execute("SELECT * FROM books JOIN authors ON books.author_id = authors.id " \
                    "WHERE "+'LOWER(name)'+" LIKE :name", {"name":'%tamora%'}).fetchall()
    for r in res: print(r)


def a7():
    db.execute("ALTER TABLE books ADD display_title VARCHAR")
    db.execute("UPDATE books SET display_title = title")
    db.execute("UPDATE books SET title = LOWER(title)")
    db.commit()


def a8():
    db.execute("ALTER TABLE authors ADD display_name VARCHAR")
    db.execute("UPDATE authors SET display_name = name")
    db.execute("UPDATE authors SET name = LOWER(name)")
    db.commit()

def a9(id):
    book = db.execute("SELECT * FROM books JOIN authors ON books.author_id = authors.id " \
                    "WHERE isbn=:id", {"id":isbn}).fetchone()
    print(book.year)


def a10():
    db.execute("ALTER TABLE books ADD id SERIAL")
    db.commit()

def a11():
    db.execute("ALTER TABLE books DROP CONSTRAINT books_pkey")
    db.execute("ALTER TABLE books ADD PRIMARY KEY (id)")
    db.commit()


def a12(bID, uID):
    rev = db.execute("SELECT * FROM reviews WHERE book_id = :bID AND user_id = :uID",
                {"bID":bID, "uID":uID}).fetchone()
    return rev


dicty = {'books': [{'id': 2410506, 'isbn': '000723368X', 'isbn13': '9780007233687', 'ratings_count': 35417, 'reviews_count': 62362, 'text_reviews_count': 1630, 'work_ratings_count': 39733, 'work_reviews_count': 70560, 'work_text_reviews_count': 2174, 'average_rating': '3.70'}]}
print(dicty['books'][0]['id'])
