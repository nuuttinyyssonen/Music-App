from app import db, generate_password_hash, check_password_hash, UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(), unique=True)
    password = db.Column(db.String())
    
    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)

class Song(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    audio = db.Column(db.String, unique=True, nullable=False)
    img = db.Column(db.String, unique=True, nullable=False)
    img_filename = db.Column(db.String, nullable=False)
    audio_filename = db.Column(db.String, nullable=False)
    audio_mimetype = db.Column(db.String, nullable=False)
    img_mimetype = db.Column(db.String, nullable=False)
    song_name = db.Column(db.String, unique=True)
    artist_name = db.Column(db.String, unique=False)
    

class Playlist(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    # song_id = db.Column(db.Integer, db.ForeignKey('song.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # song = db.relationship("Song", foreign_keys='Playlist.song_id')
    songs = db.relationship("PlaylistSongs", backref='playlist')
    user = db.relationship("User", foreign_keys='Playlist.user_id')
    playlist_name = db.Column(db.String, unique=False)

class PlaylistSongs(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    playlist_id = db.Column(db.Integer, db.ForeignKey('playlist.id'))
    song_id = db.Column(db.Integer, db.ForeignKey('song.id'))
    song = db.relationship("Song", foreign_keys='PlaylistSongs.song_id')
