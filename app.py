from datetime import date, timedelta
from flask import Flask, flash, render_template, request, redirect, url_for, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from importlib_metadata import method_cache
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
import sys

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:mynewpassword@localhost:5432/project_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SECRET_KEY'] = 'thisisasecretkey'
Bcrypt = Bcrypt(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return Account.query.get(int(user_id))


class Account(db.Model, UserMixin):
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    number_of_sanctions = db.Column(db.Integer, nullable=False)
    is_active = db.Column(db.Boolean, nullable=False)
    email = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False)

    books = db.relationship("Book", backref="account")

    def __init__(self, first_name: str, last_name: str, username: str, password: str, number_of_sanctions: int,
                 is_active: bool, email: str, is_admin: bool):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.password = password
        self.number_of_sanctions = number_of_sanctions
        self.is_active = is_active
        self.email = email
        self.is_admin = is_admin


class Book(db.Model):
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    ISBN = db.Column(db.String, nullable=False)
    title = db.Column(db.String, nullable=False)
    subject = db.Column(db.String, nullable=False)
    language = db.Column(db.String, nullable=False)
    number_of_pages = db.Column(db.Integer, nullable=False)
    publication_date = db.Column(db.Date, nullable=False)
    publisher = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    due_date = db.Column(db.Date)
    borrowed_date = db.Column(db.Date)

    author_id = db.Column(db.Integer, db.ForeignKey("author.id"), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey("account.id"), nullable=True)

    def __init__(self, ISBN : str, title : str, subject : str, language : str, 
                number_of_pages : int, publication_date : date, publisher : str, price : int, 
                due_date : date, borrowed_date : date, author_id : int):
        self.ISBN = ISBN
        self.title = title
        self.subject = subject
        self.language = language
        self.number_of_pages = number_of_pages
        self.publication_date = publication_date
        self.publisher = publisher
        self.price = price
        self.due_date = due_date
        self.borrowed_date = borrowed_date
        self.author_id = author_id

class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    dob = db.Column(db.Date, nullable=False)
    books = db.relationship("Book", backref="author")

    def __init__(self, name : str, dob : date):
        self.name = name
        self.dob = dob


class LoginForm(FlaskForm):
    username = StringField(validators=[
        InputRequired()])

    password = PasswordField(validators=[
        InputRequired()])

    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    firstName = StringField(validators=[
                           InputRequired()])
    lastName = StringField(validators=[ 
                           InputRequired()])
    username = StringField(validators=[
                           InputRequired()])
    password = PasswordField(validators=[
                             InputRequired()])
    email = StringField(validators=[
                           InputRequired()])

    def validate_username(self, username):
        existing_user_username = Account.query.filter_by(username=username.data).first()
        if existing_user_username:
            raise ValidationError('That username already exists. Please choose a different one.')

    def validate_email(self, email):
        user = Account.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

@app.route('/home')
def home():
    return render_template('home.html')


@app.route("/home/search", methods=["GET"])
def search():
    error = False
    response = []
    try:
        # Obtain all the books from the database and send it to js
        books = Book.query.order_by("id").all()
        for book in books:
            author_name = Author.query.get(int(book.author_id)).name
            response.append({"id": book.id, "title": book.title, "price": book.price, "authorName": author_name})
    except Exception as e:
        error = True
        print(e)
        print(sys.exc_info())

    if error:
        abort(500)
    else:
        return jsonify(response)


@app.route("/home/rent", methods=["POST"])
def rent():
    error = False
    no_books = False
    succesfull_rent = False
    already_rented_by_current_user = False
    try:
        requestData = request.get_json()
        id_rent_books = requestData["idBooksToRent"]
        if current_user.is_authenticated:
            if len(id_rent_books) != 0:
                for id in id_rent_books:
                    book = Book.query.get(int(id))
                    # Success
                    if book.user_id == None:
                        book.user_id = int(current_user.id)
                        book.borrowed_date = date.today()
                        book.due_date = date.today() + timedelta(days=7)
                        succesfull_rent = True
                    elif book.user_id == current_user.id:
                        already_rented_by_current_user = True
                    else:
                        succesfull_rent = False
                db.session.commit()
            else:
                no_books = True
    except Exception as e:
        error = True
        print(e)
        print(sys.exc_info())
        db.session.rollback()
    finally:
        db.session.close()

    return jsonify({"noBooks": no_books, "succesfullRent": succesfull_rent, "alreadyRentedByCurrentUser": already_rented_by_current_user})


@app.route("/")
def index():
    return redirect(url_for('home'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    error = False
    try:
        form = RegisterForm()
        if form.validate_on_submit():
            hashed_password = Bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            new_user = Account(first_name=form.firstName.data, 
            last_name=form.lastName.data, 
            number_of_sanctions=0,is_active=True,
            username=form.username.data, 
            password=hashed_password, 
            email=form.email.data,
            is_admin=False)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
    except Exception as e:
        error = True
        print(e)
        print(sys.exc_info())
    if error:
        abort(500)
    else:
        return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = False
    try:
        form = LoginForm()
        if form.validate_on_submit():
            user = Account.query.filter_by(username=form.username.data).first()
            if user is not None:
                if user:
                    if Bcrypt.check_password_hash(user.password, form.password.data):
                        login_user(user)
                        return redirect(url_for('home'))
                else:
                    flash("Invalid password!", "error")        
    except Exception as e:
        error = True
        print(e)
        print(sys.exc_info())

    if error:
        abort(500)
    else:
        return render_template('login.html', form=form)


@app.route("/logout", methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/settings")
@login_required
def settings():
    return render_template("settings.html")


@app.route("/settings/newPassword", methods=['POST'])
def update_password():
    try:
        if request.method == "POST":
            newPassword = request.form.get("newPassword")
            user_id = current_user.id
            newHash = Bcrypt.generate_password_hash(newPassword).decode('utf-8')
            account = Account.query.filter_by(id=user_id).first()
            account.password = newHash 
            db.session.commit()
    except:
        db.session.rollback()

    return redirect(url_for('home')) 


@app.route("/settings/deleteUser", methods=["POST"])
def delete_user():
    try:
        user_id = current_user.id
        account_to_delete = Account.query.filter_by(id = user_id).first()
        db.session.delete(account_to_delete)
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
        return render_template("home.html")


@app.route("/add_book")
@login_required
def add_book():
    return render_template("add_book.html", authors=Author.query.all())


@app.route("/add_book/new", methods=["POST"])
def add_book_new():
    book_already_exists = False
    error = False
    try:
        requestData = request.get_json()
        ISBN = requestData["ISBN"]
        title = requestData["title"]
        subject = requestData["subject"]
        language = requestData["language"]
        numberOfPages = requestData["numberOfPages"]
        publicationDate = requestData["publicationDate"]
        publisher = requestData["publisher"]
        price = requestData["price"]
        author_id = requestData["author_id"]

        q = db.session.query(Book.id).filter(Book.ISBN == ISBN)
        if (db.session.query(q.exists()).scalar()):
            book_already_exists = True
            pass
        else:
            book = Book(ISBN=ISBN, title=title, subject=subject, language=language, number_of_pages=numberOfPages,
                        publication_date=publicationDate, publisher=publisher, price=price, due_date=None, borrowed_date=None, author_id=author_id)
            db.session.add(book)
            db.session.commit()
    except Exception as e:
        error = True
        print(e)
        print(sys.exc_info())
        db.session.rollback()
    finally:
        db.session.close()

    if error:
        abort(500)
    else:
        return jsonify({"book_already_exists": book_already_exists})

@app.route("/add_author")
@login_required
def add_author():
    return render_template("add_author.html")


@app.route("/add_author/new", methods=["POST"])
def add_author_new():
    author_already_exists = False
    error = False
    try:
        requestData = request.get_json()
        name = requestData["name"]
        dob = requestData["dob"]

        q = db.session.query(Author.id).filter(Author.name == name and Author.dob == dob)
        if (db.session.query(q.exists()).scalar()):
            author_already_exists = True
            pass
        else:
            author = Author(name=name, dob=dob)
            db.session.add(author)
            db.session.commit()
    except Exception as e:
        error = True
        print(e)
        print(sys.exc_info())
        db.session.rollback()
    finally:
        db.session.close()

    if error:
        abort(500)
    else:
        return jsonify({"author_already_exists": author_already_exists})


# Error handling
@app.errorhandler(401)
def unauthorized(e):
    return render_template("401.html")


@app.errorhandler(403)
def forbidden(e):
    return render_template("403.html")


@app.errorhandler(404)
def not_found(e):
    return render_template("404.html")


@app.errorhandler(500)
def server_error(e):
    app.logger.error(f"Server error: {e}, route: {request.url}")
    return render_template("500.html")

if __name__ == "__main__":
    app.run(debug=True, port=5001)
