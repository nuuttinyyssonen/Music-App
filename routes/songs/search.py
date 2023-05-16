from flask import request, render_template, Blueprint
from ...models.models import Song

search_bp = Blueprint('search_bp', __name__)

@search_bp.route('/search', methods=['GET', 'POST'])
def search():
	searchBtn = request.form.get('searchBtn', False)
	searchInput = request.form.get('search')
	songs = ""

	if searchBtn != False:
		songs = Song.query.filter(Song.song_name.like('%' + searchInput + '%'))

	return render_template('./main/search.html', songs=songs)