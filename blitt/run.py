from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm, SellingForm
#from flask_login import current_user
from models import User, Post

app = Flask(__name__)
app.config['SECRET_KEY'] = 'f43dc2a8f5b0d1f89c21a96456fa598d'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
#login_manager = LoginManager(app)

#@login_manager.user_loader
#def load_user(user_id):
#	return User.query.get(int(user_id))

posts = [
{
	'seller': 'Jesse Thomas',
	'title': 'Hey',
	'content': 'some shit',
	'date_posted': 'Feb 1, 2020'
},
{
	'seller': 'Jesse Thomas',
	'title': 'Hey 2',
	'content': 'What is uppppppppp? ',
	'date_posted': 'Feb 1, 2020'
}
]

@app.route('/')
@app.route('/home')
def home():
	return render_template('home.html', posts=posts)

@app.route('/dashboard')
def dashboard():
	return render_template('dashboard.html', posts=posts)

@app.route('/login.html', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and (user.password == form.password.data):
			flash(f'Welcome, {user.username}!', 'success')
			return redirect(url_for('dashboard'))
		flash(f'Login Unsuccessful, please check username and password.', 'danger')
	return render_template('login.html', title='Login', form=form)

@app.route('/register.html', methods=['GET', 'POST'])
def register():
	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(username=form.username.data, email=form.email.data, password=form.password.data)
		db.session.add(user)
		db.session.commit()
		flash(f'Welcome to Blitt, {user.username}! You may now login.', 'success')
		return redirect(url_for('login'))
	return render_template('register.html', title='Register', form=form) 

@app.route('/profile')
def profile():
	return render_template('profile.html')

@app.route('/selling', methods=['GET', 'POST'])
def selling():
	form = SellingForm()
	if form.validate_on_submit():
		flash(f'Your listing was posted!', 'success')
		return redirect(url_for('dashboard'))
	return render_template('selling.html', title='Sell', form=form)

if __name__ == '__main__':
	app.run(debug=True)