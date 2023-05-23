from flask import Blueprint, redirect, render_template, url_for, request, flash
from ...extensions.forms import Signup
from ...models.models import User
from ...extensions.extensions import db

signup_bp = Blueprint('signup_bp', __name__)

@signup_bp.route('/signup', methods=['GET', 'POST'])
def signup():
	form = Signup()
	if request.method == 'POST':

		try:
			email = form.email.data
			user = User(email=email)
			user.set_password(form.password.data)
			db.session.add(user)
			db.session.commit()
			return redirect(url_for('login_bp.login'))
		except:
			flash('This email is already in use!')
			print('This email is already in use!')
			return redirect(url_for('signup_bp.signup'))
		
	return render_template('./auth/signup.html', form=form)