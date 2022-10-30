from app import db, lm
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    author = db.relationship("User", backref="posts", lazy=True)
    title = db.Column(db.String(50))
    description = db.Column(db.String(200))
    content = db.Column(db.Text)
    cover = db.Column(db.Text)
    views = db.Column(db.Integer, default=0)
    published_date = db.Column(db.DateTime)


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
        self.name = form['user_name']
        self.email = form['user_email']
        if form['user_password'] == form['user_password_2']:
            self.password = generate_password_hash(form['user_password'])
            self.created_date = datetime.now()
            return "YES"
        else:
            return "NO"

    def check_password(self, password):
        return self.password == generate_password_hash(password)
