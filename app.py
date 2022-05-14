from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import sys

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:1234@localhost:5432/project_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Account(db.Model):
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    number_of_sanctions = db.Column(db.Integer, nullable=False)
    is_active = db.Column(db.Boolean, nullable=False)
    email = db.Column(db.String, nullable=False)

    books = db.relationship("Book", backref="account")


class Book(db.Model):
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    ISBN = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String, nullable=False)
    subject = db.Column(db.String, nullable=False)
    language = db.Column(db.String, nullable=False)
    number_of_pages = db.Column(db.Integer, nullable=False)
    publication_date = db.Column(db.Date, nullable=False)
    publisher = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    due_date = db.Column(db.Date)
    borrowed_date = db.Column(db.Date)

    author_id = db.Column(db.Integer, db.ForeignKey("author.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("account.id"), nullable=False)


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    dob = db.Column(db.Date, nullable=False)
    books = db.relationship("Book", backref="author")

@app.route('/')
def base():
    return redirect(url_for('home'))


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/register/newUser', methods=['POST'])
def registerNewUser():
    try:

        requestData = request.get_json()
        firstName = requestData["firstName"]
        lastName = requestData["lastName"]
        username = requestData["username"]
        password = requestData["password"]
        email = requestData["email"]

        q = db.session.query(Account.id).filter(Account.username == username)
        if (db.session.query(q.exists()).scalar()):
            pass
        else:
            account = Account(first_name=firstName, last_name=lastName, username=username, password=password,
                              number_of_sanctions=0, is_active=True, email=email)
            db.session.add(account)
            db.session.commit()

    except Exception as e:
        print(e)
        print(sys.exc_info())
        db.session.rollback()
    finally:
        db.session.close()
    return "success"


if __name__ == "__main__":
    app.run(debug=True)
