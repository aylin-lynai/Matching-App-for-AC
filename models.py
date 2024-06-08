from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship


flask_app = Flask(__name__)
flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(flask_app)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    reactions = relationship("Reaction", back_populates="user")

class Image(db.Model):
    __tablename__ = 'images'
    id = db.Column(db.Integer, primary_key=True)
    image_path = db.Column(db.String(255), unique=True, nullable=False)
    reactions = relationship("Reaction", back_populates="image")

class Reaction(db.Model):
    __tablename__ = 'reactions'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    image_id = db.Column(db.Integer, db.ForeignKey('images.id'), nullable=False)
    reaction_value = db.Column(db.Boolean, nullable=False) # use db.Integer later for different reactions
    # alternative for only boolean reactions: is_positive = db.Column(db.Boolean, nullable=False), is_neutral, is_negative
    # confidence = db.Column(db.Float, nullable=False) - depending on emotion detection use this as confidence of the emotion
    user = relationship("User", back_populates="reactions")
    image = relationship("Image", back_populates="reactions")

class Match(db.Model):
    __tablename__ = 'matches'
    id = db.Column(db.Integer, primary_key=True)
    image_id = db.Column(db.Integer, db.ForeignKey('images.id'))
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.now())

class UserMatch(db.Model):
    __tablename__ = 'user_matches'
    id = db.Column(db.Integer, primary_key=True)
    user_id_1 = db.Column(db.Integer, db.ForeignKey('users.id'))
    user_id_2 = db.Column(db.Integer, db.ForeignKey('users.id'))
    match_score = db.Column(db.Float, nullable=False)
    matched_at = db.Column(db.TIMESTAMP, server_default=db.func.now())

# Verschiebe db.create_all() in einen Anwendungskontext
if __name__ == '__main__':
    with flask_app.app_context():
        db.create_all()
