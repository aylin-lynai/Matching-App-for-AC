from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy import UniqueConstraint


flask_app = Flask(__name__)
flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(flask_app)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    reactions = relationship("Reaction", back_populates="user")
    user_matches_1 = relationship("UserMatch", back_populates="user1", foreign_keys="[UserMatch.user_id_1]")
    user_matches_2 = relationship("UserMatch", back_populates="user2", foreign_keys="[UserMatch.user_id_2]")

# Methods required by Flask-Login
    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)
    
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
    happiness_score = db.Column(db.Integer, nullable=False)
    user = relationship("User", back_populates="reactions")
    image = relationship("Image", back_populates="reactions")

    __table_args__ = (UniqueConstraint('user_id', 'image_id', name='_user_image_uc'),)


class Match(db.Model):
    __tablename__ = 'matches'
    id = db.Column(db.Integer, primary_key=True)
    image_id = db.Column(db.Integer, db.ForeignKey('images.id'))
    match_score = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.now())
    user_matches = db.relationship("UserMatch", back_populates="match")

class UserMatch(db.Model):
    __tablename__ = 'user_matches'
    id = db.Column(db.Integer, primary_key=True)
    user_id_1 = db.Column(db.Integer, db.ForeignKey('users.id'))
    user_id_2 = db.Column(db.Integer, db.ForeignKey('users.id'))
    match_id = db.Column(db.Integer, db.ForeignKey('matches.id'))
    user1 = db.relationship("User", back_populates="user_matches_1", foreign_keys=[user_id_1])
    user2 = db.relationship("User", back_populates="user_matches_2", foreign_keys=[user_id_2])
    match = db.relationship("Match", back_populates="user_matches")

    def __repr__(self):
        return f"<UserMatch(user_id_1={self.user_id_1}, user_id_2={self.user_id_2}, match_id={self.match_id})>"

if __name__ == '__main__':
    with flask_app.app_context():
        db.create_all()
