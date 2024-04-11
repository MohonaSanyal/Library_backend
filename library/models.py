from . import db
from flask_login import UserMixin
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    isAdmin = db.Column(db.Boolean)
    name = db.Column(db.String(100))
    last_visited = db.Column(db.DateTime)

class Issue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_issued = db.Column(db.DateTime)
    return_date = db.Column(db.DateTime)
    book_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)

class IssueRequests(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    feedback = db.Column(db.String(100))

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    ebook_price = db.Column(db.Integer)
    authors = db.Column(db.String(100))
    content = db.Column(db.String(150))
    section_id = db.Column(db.Integer)

class Section(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    desc = db.Column(db.String(150))
    date_created = db.Column(db.DateTime)
