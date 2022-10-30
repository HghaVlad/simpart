from flask import render_template, redirect, url_for, request, flash
from app import app
from app.models import User
from flask_login import current_user, login_user


@app.route('/')
@app.route("/index")
def index():
	return render_template("index.html")


@app.route("/about")
def home_page():
	return render_template("about_me.html")


@app.route("/login")
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
	if user is None or not user.check_password(password):
		flash("Invalid email or password")
		return render_template("login.html")
	else:
		login_user(user)
		return "<b>Successful login</b>"


@app.route("/logup")
def reg_page():
	if current_user.is_authenticated:
		return redirect(url_for("index"))
	else:
		return render_template("reg.html")
