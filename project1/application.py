import os, json 
import requests
from flask import Flask, session, render_template, request, jsonify, flash, redirect
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
key = os.getenv("key")


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register")
def register():    
    return render_template("register.html")

@app.route("/login")
def login():    
    return render_template("login.html")

@app.route("/authenticate", methods=["POST"])
def authenticate():
    
    username = request.form.get("username")
    password = request.form.get("password")
    if username.strip() == "":
        return render_template("register.html", message1="Please enter a valid username")
       
    elif password.strip() == "":
        return render_template("register.html", message2="Please enter a valid password")

    if db.execute("SELECT * FROM LOGIN  WHERE USERNAME = :username", {"username": username}).rowcount >= 1:    
        return render_template("register.html", message1="Username already taken")
    db.execute("INSERT INTO LOGIN(USERNAME,PASSWORD) VALUES(:username, :password)",
                {"username": username, "password": password})
    db.commit()
    return render_template("success.html")
   

@app.route("/verify", methods=["GET", "POST"])  
def verify(): 
    if session.get("username") is None:
       session["username"] = []
       session["user_id"] = []  
    if request.method == "POST":
       username = request.form.get("username")
       password = request.form.get("password")
       if username.strip() == "":
          return render_template("login.html", message1="Please enter a valid username")
       
       elif password.strip() == "":
          return render_template("login.html", message2="Please enter a valid password")
    
       if db.execute("SELECT * FROM LOGIN WHERE USERNAME = :username AND PASSWORD = :password", {"username": username, "password": password}).rowcount == 0:
          return render_template("login.html", message="THE Username or password you typed is incorrect, please try again.")
       user_id = db.execute("SELECT id FROM LOGIN WHERE USERNAME = :username AND PASSWORD = :password", {"username": username, "password": password}).fetchone()
       session["user_id"] = user_id 
       session["username"].append(username)
       return render_template("bookreview.html", username= username)

@app.route("/logout")   
def logout():  
    session.pop("user_id", None) 
    session.pop("username", None) 
    return render_template("index.html")

@app.route("/search", methods=["GET", "POST"])  
def search():
    for i in session["username"]:
        user = i
    name = request.form.get("name") 
    name = str(name)
    if name.strip() == "":
        return render_template("bookreview.html", username= user, message= "Please enter a valid isbn number, book title or name of an author") 
    if db.execute("SELECT * FROM books WHERE isbn = :name OR title = :name OR author = :name",{"name": name} ).rowcount >= 1:
        books = db.execute("SELECT * FROM books WHERE isbn = :name OR title = :name OR author = :name",{"name": name} ).fetchall()
        return render_template("bookreview.html", username= user, books = books, message= "RESULT")
    name = '%'+name+'%' 
    if db.execute("SELECT * FROM books WHERE isbn LIKE :name OR title LIKE :name OR author LIKE :name ",{"name": name} ).rowcount != 0:
        books = db.execute("SELECT * FROM books WHERE isbn LIKE :name OR title LIKE :name OR author LIKE :name ",{"name": name} ).fetchall()
        return render_template("bookreview.html", username= user, books = books, message= "RESULT")
    return render_template("bookreview.html", username= user, message= "Sorry, the book you are searching for does not exist in our database")

@app.route("/book_page/<int:book_id>", methods=["GET", "POST"])  
def book_page(book_id):  
    for i in session["username"]:
        user = i
    session["book_id"] = []
    session["book_id"].append(book_id) 
    book = db.execute("SELECT * FROM books WHERE id = :id", {"id": book_id}).fetchone()
    res = requests.get("https://www.goodreads.com/book/review_counts.json",
                       params={"key":key, "isbns": book.isbn})
    if res.status_code != 200:
        raise Exception("ERROR: API request unsuccessful.")
    data = res.json()
    average_rating = data['books'][0]['average_rating']
    work_ratings_count = data['books'][0]['work_ratings_count']
    if book is None:
        return render_template("error.html", message="No such book exists in our database.")
    pre_reviews = db.execute("SELECT * FROM reviews WHERE review_id = :id", {"id": book_id}).fetchall()  
    return render_template("book_page.html", book = book, average_rating = average_rating, work_ratings_count = work_ratings_count, pre_reviews= pre_reviews, username= user)

@app.route("/book_review", methods=["GET", "POST"])  
def book_review():  
    for i in session["username"]:
        user = i
    for z in session["user_id"]:
        current_user = z 
    for l in session["book_id"]:
        book_id = l 
    #current_user =  db.execute("SELECT id FROM LOGIN WHERE username = :i", {"i": user}).fetchone()   
    book = db.execute("SELECT * FROM books WHERE id = :id", {"id": book_id}).fetchone()               
    review = request.form.get("review")
    rating = request.form.get("rating")
    pre_reviews = db.execute("SELECT * FROM reviews WHERE review_id = :id", {"id": book_id}).fetchall()  
    res = requests.get("https://www.goodreads.com/book/review_counts.json",
                       params={"key":key, "isbns": book.isbn})
    if res.status_code != 200:
        raise Exception("ERROR: API request unsuccessful.")
    data = res.json()
    average_rating = data['books'][0]['average_rating']
    work_ratings_count = data['books'][0]['work_ratings_count']
    
    if review.strip() == "":
          return render_template("book_page.html", book = book, username= user,average_rating = average_rating, work_ratings_count = work_ratings_count, pre_reviews= pre_reviews, rating=rating, message1="Please enter a review before you click submit.")
       
    elif rating is None:
          return render_template("book_page.html", book = book, username= user, average_rating = average_rating, work_ratings_count = work_ratings_count,pre_reviews= pre_reviews, rating=rating, message2="Please give the book a rating before you click submit.")
    
    if db.execute("SELECT * FROM reviews WHERE user_review = :id AND review_id = :rd", {"id": current_user, "rd": book_id}).rowcount >= 1:
             return render_template("error.html", message="You have already submitted a review for this book.")
    db.execute("INSERT INTO reviews (review, rating, review_id, user_review) VALUES (:review, :rating, :book_id, :user_id)",
            {"review": review, "rating": rating, "book_id": book_id, "user_id": current_user })  
    db.commit()
    return render_template("successful.html")

@app.route("/api/<isbn>")
def book_api(isbn):
    """Return details about a single flight."""

    # Make sure flight exists.
    book = db.execute("SELECT * FROM books WHERE id = :id", {"id": isbn}).fetchone()
    res = requests.get("https://www.goodreads.com/book/review_counts.json",
                       params={"key":key, "isbns": isbn})
    if res.status_code != 200:
        raise Exception("ERROR: API request unsuccessful.")
    data = res.json()
    average_rating = data['books'][0]['average_rating']
    work_ratings_count = data['books'][0]['work_ratings_count']
    if book is None:
        return jsonify({"error": "Invalid ISBN number"}), 422

    # Get all passengers.
    
    return jsonify({
            "title": book.title,
            "author": book.author,
            "year": book.year,
            "isbn": isbn,
            "review_count": work_ratings_count,
            "average_score": average_rating
        })
