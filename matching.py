from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from models import db, User, Image, Reaction, flask_app
from happiness_detector import handle_reactions
import random


def create_dummy_data():
    with flask_app.app_context():
        db.create_all()
        
        # Create 4 users
        users = [
            User(username='user1', email='user1@example.com'),
            User(username='user2', email='user2@example.com'),
            User(username='user3', email='user3@example.com'),
            User(username='user4', email='user4@example.com')
        ]
        
        for user in users:
            if not User.query.filter_by(email=user.email).first():
                db.session.add(user)
        
        image_paths = [f'image_{i}.jpg' for i in range(1, 11)]
        existing_images = {image.image_path for image in Image.query.all()}

        for image_path in image_paths:
            if image_path not in existing_images:
                db.session.add(Image(image_path=image_path))
        
        #db.session.commit()

        # Create reactions
        for user in users:
           handle_reactions(user.id, image_paths)
        
        db.session.commit()

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
