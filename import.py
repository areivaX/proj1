import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


def b1():
    db.execute("CREATE TABLE authors (id SERIAL PRIMARY KEY, name VARCHAR NOT NULL) ")
    db.commit()

def b0():
    db.execute("CREATE TABLE users (user_id SERIAL PRIMARY KEY, email VARCHAR UNIQUE, username VARCHAR UNIQUE, password VARCHAR)")

def b3():
    db.execute("CREATE TABLE reviews (review_id SERIAL PRIMARY KEY, book_id INTEGER REFERENCES books, " \
                "user_id INTEGER REFERENCES users, rating INTEGER, text VARCHAR, " \
                "CONSTRAINT rating_values CHECK (rating>0 AND rating<6) )")
    db.commit()

def b2():
    db.execute("CREATE TABLE books " \
                    "(book_id SERIAL PRIMARY KEY, isbn VARCHAR UNIQUE, "\
                    "title VARCHAR, year INTEGER, "\
                    "author_id INTEGER REFERENCES authors )")
    db.commit()

def b4():
    #we assume that no two authors have the same name, since given books.csv we wouldn't be able to tell if not
    db.execute("ALTER TABLE authors ADD CONSTRAINT a_name unique(name)")
    db.commit()

def a1():
    f = open("books.csv")
    reader = csv.reader(f)
    fields = next(reader)
    count = 0
    for line in reader:
        count +=1
        auth_name = line[2]
        if db.execute("SELECT * FROM authors WHERE name = :name", {"name": auth_name}).fetchone() is None:
            db.execute('INSERT INTO authors (name) VALUES (:author)', {"author":auth_name})
            print(f"inserting on count {count}")
    db.commit()




def a2():
    f = open("books.csv")
    #suppose there are no book duplicates
    reader = csv.reader(f)
    fields = next(reader)
    for line in reader:
        isbn,title,author,year = line
        print(f"looking for {author}")
        x = db.execute("SELECT * FROM authors WHERE name = :author", {"author":author}).first()
        author_id = x.id

        db.execute("INSERT INTO books (isbn, title, year, author_id) VALUES " \
                    "(:isbn, :title, :year, :author_id)",
                    {"isbn":isbn, "title":title, "year":year, "author_id":author_id})
    db.commit()





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

def main():
    #b0()
    #b1(),
    #b2(),
    #b3(), #b4()
    a1(), a2(), a7(), a8()

if __name__ == "__main__":
    main()
