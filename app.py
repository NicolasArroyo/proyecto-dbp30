import json
from flask import Flask, flash, render_template, request, redirect, url_for, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
import sys

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:mynewpassword@localhost:5432/project_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SECRET_KEY'] = 'thisisasecretkey'

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

    books = db.relationship("Book", backref="account")

    def __init__ (self, first_name : str, last_name : str, username : str, password : str, number_of_sanctions : int, is_active : bool, email : str):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.password = password
        self.number_of_sanctions = number_of_sanctions
        self.is_active = is_active
        self.email = email


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

    
class LoginForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired()])

    password = PasswordField(validators=[
                             InputRequired()])

    submit = SubmitField('Login')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/')
def index():
    return redirect(url_for('home'))

@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/register/newUser', methods=['POST'])
def registerNewUser():
    user_already_exists = False
    error = False
    try:
        requestData = request.get_json()
        firstName = requestData["firstName"]
        lastName = requestData["lastName"]
        username = requestData["username"]
        password = requestData["password"]
        email = requestData["email"]

        q = db.session.query(Account.id).filter(Account.username == username)
        if (db.session.query(q.exists()).scalar()):
            user_already_exists = True
            pass
        else:
            account = Account(first_name=firstName, last_name=lastName, username=username, password=password,
                              number_of_sanctions=0, is_active=True, email=email)
            db.session.add(account)
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
        return jsonify({"user_already_exists": user_already_exists})


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = False
    try:
        form = LoginForm()
        if form.validate_on_submit():
            user = Account.query.filter_by(username=form.username.data).first()
            if user is not None:
                if user:
                    password = Account.query.filter_by(password=form.password.data).first()
                    if password:
                        login_user(user)
                        return redirect(url_for('home'))
    except Exception as e:
        error = True
        print(e)
        print(sys.exc_info())

    if error:
        abort(500)
    else:
        return render_template('login.html', form=form)


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/settings")
@login_required
def settings():
    return render_template("settings.html")

@app.route("/settings/newPassword", methods=['POST'])
def update_password():
    correct_username_password = True
    try:
        requestData = request.get_json()
        username = requestData["username"]
        new_password = requestData["newPassword"]
        current_password = requestData["password"]
        q = db.session.query(Account.id).filter(Account.username == username, Account.password == current_password)
        if (db.session.query(q.exists()).scalar()):
            account = Account.query.filter_by(username=username, password=current_password).first()
            account.password = new_password
            db.session.commit()
        else:
            correct_username_password = False
    except:
        db.session.rollback()
    finally:
        db.session.close()

    return jsonify({"correctUsernamePassword": correct_username_password})


@app.route("/settings/deleteUser", methods=["POST"])
def delete_user():
    correct_username_password = True
    try:
        requestData = request.get_json()
        username = requestData["username"]
        password = requestData["password"]
        account_to_delete = Account.query.filter_by(username=username, password=password).first()

        q = db.session.query(Account.id).filter(Account.username == username, Account.password == password)
        if (db.session.query(q.exists()).scalar()):
            db.session.delete(account_to_delete)
            db.session.commit()
        else:
            correct_username_password = False
    except:
        db.session.rollback()
    finally:
        db.session.close()
    
    return jsonify({"correctUsernamePassword": correct_username_password})


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