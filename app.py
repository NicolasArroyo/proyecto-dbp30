import json
from flask import Flask, flash, render_template, request, redirect, url_for, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, ValidationError
from flask_bcrypt import Bcrypt
import sys

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:1234@localhost:5432/project_db"
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

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/')
def index():
    return redirect(url_for('home'))

@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    error = False
    try:
        form = RegisterForm()
        if form.validate_on_submit():
            hashed_password = Bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            new_user = Account(firstName=form.firstName.data, 
            lastName=form.lastName.data, 
            number_of_sanctions=0,is_active=True,
            username=form.username.data, 
            password=hashed_password, 
            email=form.email.data)
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
    
    print(correct_username_password )

    # return redirect(url_for("index"))
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

if __name__ == "__main__":
    app.run(debug=True, port=5001)
