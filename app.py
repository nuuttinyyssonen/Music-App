from flask import Flask, redirect, url_for, render_template, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, logout_user, LoginManager, login_required
from decouple import config
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename
from forms import *
from custom import *

app = Flask(__name__)
app.config['SECRET_KEY'] = config('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///my_database.db'

db = SQLAlchemy(app)
from models import *

login = LoginManager(app)
login.login_view = 'login'

@app.before_first_request
def create_tables():
    db.create_all()

@login.user_loader
def load_user(id):
  return User.query.get(int(id))

app.jinja_env.filters['b64encode'] = b64encode

@app.route('/', methods=['GET', 'POST'])
def login():
	form = Login()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()

		if user is None or not user.check_password(form.password.data):
			flash('Invalid Password or Email')
			print("Invalid Password or Email")
			return redirect(url_for('login'))
		
		login_user(user)
		next_page = request.args.get('next')

		if not next_page or url_parse(next_page).netloc != '':
			print('working')
			next_page = url_for('main')
		return redirect(next_page)
   
	return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
	form = Signup()
	if form.validate_on_submit():
		email = form.email.data
		user = User(email=email)
		user.set_password(form.password.data)
		db.session.add(user)
		db.session.commit()
		return redirect(url_for('login'))
	return render_template('signup.html', form=form)

@app.route('/main', methods=['GET', 'POST'])
def main():
   all_audio = Audio.query.all()
   return render_template('main.html', all_audio=all_audio)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
	uploadBtn = request.form.get('submit', False)

	if uploadBtn != False:
		audio = request.files['audio']

		if not audio:
			return 'No pic uploaded', 400

		filename = secure_filename(audio.filename)
		mimetype = audio.mimetype

		db.session.expunge_all()

		audioFile = Audio(audio=audio.read(), mimetype=mimetype, name=filename)
		db.session.add(audioFile)
		db.session.commit()

	return render_template('upload.html')