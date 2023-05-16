from flask import Blueprint, redirect, render_template, url_for
from ...extensions.forms import Signup
from ...models.models import User
from ...extensions.extensions import db

signup_bp = Blueprint('signup_bp', __name__)

@signup_bp.route('/signup', methods=['GET', 'POST'])
def signup():
	form = Signup()
	if form.validate_on_submit():
		email = form.email.data
		user = User(email=email)
		user.set_password(form.password.data)
		db.session.add(user)
		db.session.commit()
		return redirect(url_for('login_bp.login'))
	return render_template('./auth/signup.html', form=form)