from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
import random

flask_app = Flask(__name__)
flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dummy-data.db'
db = SQLAlchemy(flask_app)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    reactions = relationship("Reaction", back_populates="user")
    user_matches_1 = relationship("UserMatch", back_populates="user1", foreign_keys="[UserMatch.user_id_1]")
    user_matches_2 = relationship("UserMatch", back_populates="user2", foreign_keys="[UserMatch.user_id_2]")

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
    reaction_value = db.Column(db.Boolean, nullable=False)
    user = relationship("User", back_populates="reactions")
    image = relationship("Image", back_populates="reactions")

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

def create_dummy_data():
    with flask_app.app_context():
        db.drop_all()
        db.create_all()
        
        users = [
            User(username='user1', email='user1@example.com'),
            User(username='user2', email='user2@example.com'),
            User(username='user3', email='user3@example.com'),
            User(username='user4', email='user4@example.com')
        ]
        
        for user in users:
            db.session.add(user)
        
        images = [Image(image_path=f'image_{i}.jpg') for i in range(1, 6)]
        
        for image in images:
            db.session.add(image)
        
        db.session.commit()

        for user in users:
            for image in images:
                reaction = Reaction(
                    user_id=user.id,
                    image_id=image.id,
                    reaction_value=random.choice([0, 1])
                )
                db.session.add(reaction)
        
        db.session.commit()
        
        print("Users:")
        for user in User.query.all():
            print(user.id, user.username, user.email)

        print("\nImages:")
        for image in Image.query.all():
            print(image.id, image.image_path)

        print("\nReactions:")
        for reaction in Reaction.query.all():
            print(reaction.id, reaction.user_id, reaction.image_id, reaction.reaction_value)

def calculate_similarity(user1, user2):
    reactions1 = {reaction.image_id: reaction.reaction_value for reaction in user1.reactions}
    reactions2 = {reaction.image_id: reaction.reaction_value for reaction in user2.reactions}
    
    common_reactions = set(reactions1.keys()) & set(reactions2.keys())
    if not common_reactions:
        return 0
    
    similarity = sum(reactions1[image_id] == reactions2[image_id] for image_id in common_reactions) / len(common_reactions)
    return similarity

def rank_users():
    with flask_app.app_context():
        users = User.query.all()
        for user in users:
            similarities = [(other_user, calculate_similarity(user, other_user)) for other_user in users if user != other_user]
            similarities.sort(key=lambda x: x[1], reverse=True)
            
            print(f"Rankings for {user.username}:")
            for rank, (other_user, similarity) in enumerate(similarities, start=1):
                print(f"{rank}. {other_user.username} (Similarity: {similarity:.2f})")

if __name__ == '__main__':
    create_dummy_data()
    rank_users()
