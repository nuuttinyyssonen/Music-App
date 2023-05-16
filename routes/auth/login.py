from flask import session, Blueprint, flash, redirect, url_for, request, render_template
from werkzeug.urls import url_parse
from flask_login import login_user
from ...extensions.forms import Login
from ...extensions.extensions import login
from ...models.models import User

login_bp = Blueprint('login_bp', __name__)
login.login_view = 'login'

@login.user_loader
def load_user(id):
  return User.query.get(int(id))

@login_bp.route('/', methods=['GET', 'POST'])
def login():
	form = Login()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		session['email'] = form.email.data

		if user is None or not user.check_password(form.password.data):
			flash('Invalid Password or Email')
			print("Invalid Password or Email")
			return redirect(url_for('login_bp.login'))
		
		login_user(user)
		next_page = request.args.get('next')

		if not next_page or url_parse(next_page).netloc != '':
			print('working')
			next_page = url_for('main_bp.main')

		return redirect(next_page)
   
	return render_template('./auth/login.html', form=form)