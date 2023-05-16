from flask import request, redirect, render_template, url_for, Blueprint
from ...models.models import Playlist, Song, PlaylistSongs
from ...extensions.extensions import db

playlist_bp = Blueprint('playlist_bp', __name__)

@playlist_bp.route('/playlist/<int:id>', methods=['GET', 'POST'])
def playlist(id):
	playlist = Playlist.query.filter_by(id=id).first()
	search = request.form.get('searchBtn', False)
	searchValue = request.form.get('search')
	songs = ""

	addBtn = request.form.get('add', False)
	song_id = request.form.get('songId')

	playlist_name_change = request.form.get('playlist-name')
	playlist_name_change_submit = request.form.get('playlist-name-submit', False)

	deletePlaylist = request.form.get('delete-playlist-btn', False)

	if deletePlaylist != False:
		db.session.delete(playlist)
		db.session.commit()
		return redirect(url_for('main_bp.main'))

	if playlist_name_change_submit != False:
		playlist.playlist_name = playlist_name_change
		db.session.commit()

	if search != False:
		songs = Song.query.filter(Song.song_name.like('%' + searchValue + '%'))

	if addBtn != False:
		song = PlaylistSongs(song_id=song_id, playlist_id=id)
		db.session.add(song)
		db.session.commit()

	playlist_songs = playlist.songs
	playlist_name = playlist.playlist_name
	for song in playlist_songs:
		print(song.song)
	
	return render_template('./main/playlist.html', playlist=playlist, songs=songs, id=id, playlist_songs=playlist_songs, playlist_name=playlist_name)