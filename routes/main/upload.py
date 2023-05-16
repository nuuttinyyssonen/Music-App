from flask import request, Blueprint, render_template
from ...extensions.extensions import db
from ...models.models import Song
from werkzeug.utils import secure_filename

upload_bp = Blueprint('upload_bp', __name__)

@upload_bp.route('/upload', methods=['GET', 'POST'])
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

	return render_template('./main/upload.html')