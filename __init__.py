from flask import Flask, session
from .models.models import User, Playlist
from decouple import config
from .extensions.custom import b64encode
from .extensions.extensions import login, db
from .routes.auth.login import login_bp
from .routes.auth.signup import signup_bp
from .routes.auth.logout import logout_bp
from .routes.main.main import main_bp
from .routes.main.upload import upload_bp
from .routes.songs.playlist import playlist_bp
from .routes.songs.search import search_bp

app = Flask(__name__)
app.config['SECRET_KEY'] = config('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///music_app.db'

db.init_app(app)
login.init_app(app)

app.jinja_env.filters['b64encode'] = b64encode

@app.before_request
def create_tables():
    db.create_all()

@app.context_processor
def utility_processor():
	no_user_list = []
	try:
		user = User.query.filter_by(email=session['email']).first()
		user_id = user.id
		playlists = Playlist.query.filter_by(user_id=user_id).all()
		return dict(playlists=playlists)
	except Exception:
		return dict(no_user_list=no_user_list)


app.register_blueprint(login_bp)
app.register_blueprint(signup_bp)
app.register_blueprint(logout_bp)
app.register_blueprint(main_bp)
app.register_blueprint(upload_bp)
app.register_blueprint(playlist_bp)
app.register_blueprint(search_bp)
