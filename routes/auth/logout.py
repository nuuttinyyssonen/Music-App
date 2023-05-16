from flask import session, redirect, url_for, Blueprint
from flask_login import login_required, logout_user

logout_bp = Blueprint('logout_bp', __name__)

@logout_bp.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
	logout_user()
	session['email'] = None
	return redirect(url_for('login_bp.login'))