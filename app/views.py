from flask import render_template, redirect, url_for, request, flash
from app import app, db
from app.models import User
from flask_login import current_user, login_user


@app.route('/')
@app.route("/index")
def index():
	return render_template("index.html")


@app.route("/about")
def home_page():
	return render_template("about_me.html")


@app.route("/login", methods=["GET", "POST"])
def login_page():
	if current_user.is_authenticated:
		return redirect(url_for("index"))
	else:
		return render_template("login.html")


@app.route("/logining", methods=["POST"])
def logining():
	if current_user.is_authenticated:
		return redirect(url_for("index"))
	email = request.form['user_email']
	password = request.form['user_password']
	user = User.query.filter_by(email=email).first()
	if user is None or user.check_password(password) is False:
		flash("Invalid email or password")
		return redirect(url_for('login_page'))
	else:
		print("well")
		remember = request.form.get('user_check_remember')
		if remember is None:
			login_user(user)
		else:
			login_user(user, remember=True)
		return "<b>Successful login</b>"


@app.route("/logup")
def reg_page():
	if current_user.is_authenticated:
		return redirect(url_for("index"))
	else:
		return render_template("reg.html")


@app.route("/regging", methods=["POST"])
def regging():
	data = request.form
	exist_user = User.query.filter_by(email=data['user_email']).first()
	if exist_user is None:
		new_user = User()
		result = new_user.reg(data)
		if result == "YES":
			db.session.add(new_user)
			db.session.commit()
			return "<b1>Successfully reg</b1>"
		else:
			flash("You have en error")
	else:
		flash("User with this email is exist")
	return redirect(url_for('/logup'))
