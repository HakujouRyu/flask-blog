from flask import Flask, render_template, url_for, flash, redirect
from decouple import config
from dotenv import load_dotenv
from forms import RegistrationForm, LoginForm
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Configuration 
load_dotenv() # To access .env
app = Flask(__name__)
app.config['SECRET_KEY'] = 'SECRET_KEY' 
app.config['SQLALCHEMY_URI'] = config('SQLALCHEMY_URI')

#initialise DAtabase
db = SQLAlchemy(app)

#Schema, to move later
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique = True, nullable=False)
    email = db.Column(db.String(120), unique = True, nullable=False)
    img_file = db.Column(db.String(20), nullable=False, default='defaut.jpeg')
    password = db.Column(db.String(60), nullable=False, default=datetime.utcnow)
    post = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.img_file}')"
        

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"
        

#Dummy data
posts = [
    {
        'author': 'Clay',
        'title': 'Post one',
        'content': 'test content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Clay',
        'title': 'Post 2',
        'content': 'test content',
        'date_posted': 'April 20, 2019'
    }
]

#Home page urls
@app.route("/#")
@app.route("/")
@app.route("/Home")
def home():
    return render_template('home.html', posts=posts)

@app.route("/about")
def about():
    return render_template('about.html', title="About")

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title="register", form=form)

@app.route("/login",methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'test@test.com' and form.password.data == 'test':
            flash('you have been logged in', 'success')
            return redirect(url_for('home'))
        else:
            flash('Log in failed', 'danger')
    return render_template('login.html', title="login", form=form)

if __name__ == '__main__':
    app.run(debug=True)