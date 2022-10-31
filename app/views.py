from flask import render_template, redirect, url_for, request, flash
from app import app, db
from app.models import User
from flask_login import current_user, login_user, login_required, logout_user


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
	print(user.check_password(password))
	if user is not None:
		if user.check_password(password) is True:
			print("well")
			remember = request.form.get('user_check_remember')
			if remember is None:
				login_user(user)
			else:
				print(remember)
				login_user(user, remember=True)
			user.login_now()
			db.session.commit()
			return redirect(url_for("my_profile"))
	flash("Invalid email or password")
	return redirect(url_for('login_page'))


@app.route("/logup", methods=["GET", "POST"])
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
			login_user(new_user)
			new_user.login_now()
			db.session.commit()
			return redirect(url_for("my_profile"))
		else:
			flash(result)
	else:
		flash("User with this email is exist")
	return redirect(url_for('reg_page'))


@app.route("/profile")
@login_required
def my_profile():
	return render_template("profile.html")


@app.route("/edit_profile")
@login_required
def edit_profile():
	return render_template("edit_profile.html")


@app.route("/editing_profile", methods=["POST", "GET"])
@login_required
def editing_profile():
	data = request.form
	user = User.query.filter_by(id=current_user.id).first()
	response = user.edit_profile(data)
	print(response)
	if response == "YES":
		db.session.commit()
		return redirect(url_for("my_profile"))
	elif response == "PASS":
		flash("You have an error in your password")
		return redirect(url_for("edit_profile"))
	else:
		flash("You have an error in completing form")
		return redirect(url_for("edit_profile"))


@app.route("/logout")
@login_required
def logout():
	logout_user()
	return redirect(url_for("index"))
