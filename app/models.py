from app import db, lm
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    author = db.relationship("User", backref="posts", lazy=True)
    title = db.Column(db.String(200))
    description = db.Column(db.String(400))
    content = db.Column(db.Text)
    cover = db.Column(db.Text, nullable=True)
    views = db.Column(db.Integer, default=0)
    published_date = db.Column(db.DateTime)

    def publish(self, title, descr, text, user):
        self.title = title
        self.description = descr
        self.content = text
        self.author = user
        self.author_id = user.id
        self.published_date = datetime.now()

    def new_visitor(self):
        self.views = self.views + 1
        db.session.commit()

@lm.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(70), nullable=False)
    password = db.Column(db.Text, nullable=False)
    created_date = db.Column(db.DateTime, nullable=False)
    last_login = db.Column(db.DateTime)

    def reg(self, form):
        if form['user_name'] == "":
            return "Please enter your name"
        if form['user_email'] == "":
            return "Please enter your email"
        self.name = form['user_name']
        self.email = form['user_email']
        if form['user_password'] == form['user_password_2'] and len(form['user_password']) >= 6:
            self.password = generate_password_hash(form['user_password'])
            self.created_date = datetime.now()
            return "YES"
        else:
            return "Your passwords do not match or their size less than 6"

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def edit_profile(self, data):
        newname = data.get("user_name")
        new_email = data.get("user_email")
        new_pass = data.get("user_new_pass")
        old_pass = data.get("user_old_pass")
        if newname is not None and newname != "":
            self.name = newname
        if new_email is not None and new_email != "":
            self.email = new_email
        print(new_pass, new_email)
        if new_pass is not None and new_pass != "":
            if check_password_hash(self.password, old_pass):
                self.password = generate_password_hash(new_pass)
            else:
                return "Password"
        return "YES"

    def login_now(self):
        self.last_login = datetime.now()
