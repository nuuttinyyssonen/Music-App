from flask import session, redirect, render_template, request, url_for, Blueprint
from ...models.models import User, Playlist, Song
from ...extensions.extensions import db

main_bp = Blueprint('main_bp', __name__)

@main_bp.route('/main', methods=['GET', 'POST'])
def main():
	playlistBtn = request.form.get('playlist', False)
	user = User.query.filter_by(email=session['email']).first()
	if playlistBtn != False:
		playlist = Playlist(playlist_name="Playlist 1", user=user)
		db.session.add(playlist)
		db.session.commit()
		return redirect(url_for('playlist_bp.playlist', id=playlist.id))

	all_audio = Song.query.all()
	return render_template('./main/main.html', all_audio=all_audio)