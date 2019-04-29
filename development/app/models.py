from app import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(30))
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.id}', '{self.email}', '{self.name}')"

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    images = db.relationship('Dataset', backref='author', lazy=True)

    def __repr__(self):
        return f"Person('{self.id}', '{self.name}')"

class Dataset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'), nullable=False)
    image_file = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f"Dataset('{self.id}', '{self.person_id}', '{self.image_file}')"
