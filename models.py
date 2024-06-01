from flask import Flask
from flask_sqlalchemy import SQLAlchemy

flask_app = Flask(__name__)
flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(flask_app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_path = db.Column(db.String(200), unique=True, nullable=False)

class Reaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    image_id = db.Column(db.Integer, db.ForeignKey('image.id'), nullable=False)
    reaction_value = db.Column(db.Integer, nullable=False)

# Verschiebe db.create_all() in einen Anwendungskontext
if __name__ == '__main__':
    with flask_app.app_context():
        db.create_all()
