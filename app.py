from flask import Flask, redirect, url_for, render_template, flash, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, logout_user, LoginManager, login_required
from decouple import config
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename
from forms import *
from custom import *
import sys
sys.setrecursionlimit(100000)

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
		session['email'] = form.email.data

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
	playlistBtn = request.form.get('playlist', False)
	user = User.query.filter_by(email=session['email']).first()
	if playlistBtn != False:
		playlist = Playlist(playlist_name="Playlist 1", user=user)
		db.session.add(playlist)
		db.session.commit()
		return redirect(url_for('playlist', id=playlist.id))

	all_audio = Song.query.all()
	return render_template('main.html', all_audio=all_audio)


@app.context_processor
def utility_processor():
	if session['email'] != "":
		user = User.query.filter_by(email=session['email']).first()
		user_id = user.id
		playlists = Playlist.query.filter_by(user_id=user_id).all()
		return dict(playlists=playlists)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
	uploadBtn = request.form.get('submit', False)

	if uploadBtn != False:
		audio = request.files['audio']
		img = request.files['img']

		song_name = request.form.get('songName')
		artist_name = request.form.get('artist')

		if not audio:
			return 'No pic uploaded', 400

		audio_filename = secure_filename(audio.filename)
		audio_mimetype = audio.mimetype

		img_filename = secure_filename(img.filename)
		img_mimetype = secure_filename(img.filename)

		db.session.expunge_all()

		audioFile = Song(audio=audio.read(), img=img.read(), audio_mimetype=audio_mimetype, img_mimetype=img_mimetype, audio_filename=audio_filename, img_filename=img_filename, song_name=song_name, artist_name=artist_name)
		db.session.add(audioFile)
		db.session.commit()

	return render_template('upload.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
	searchBtn = request.form.get('searchBtn', False)
	searchInput = request.form.get('search')
	songs = ""

	if searchBtn != False:
		songs = Song.query.filter(Song.song_name.like('%' + searchInput + '%'))

	return render_template('search.html', songs=songs)

@app.route('/playlist/<int:id>', methods=['GET', 'POST'])
def playlist(id):
	playlist = Playlist.query.filter_by(id=id).first()
	search = request.form.get('searchBtn', False)
	searchValue = request.form.get('search')
	songs = ""
	addBtn = request.form.get('add', False)
	song_id = request.form.get('songId')

	if search != False:
		songs = Song.query.filter(Song.song_name.like('%' + searchValue + '%'))

	if addBtn != False:
		song = PlaylistSongs(song_id=song_id, playlist_id=id)
		db.session.add(song)
		db.session.commit()

	playlist_songs = playlist.songs
	for song in playlist_songs:
		print(song.song)
	

	return render_template('playlist.html', playlist=playlist, songs=songs, id=id, playlist_songs=playlist_songs)