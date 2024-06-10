from models import db, User, Image, Reaction, flask_app as app
from faker import Faker
import random

# Initialize Faker
faker = Faker()

# Function to add dummy users
def add_dummy_users(num_users=10):
    for _ in range(num_users):
        user = User(
            username=faker.user_name(),
            email=faker.email()
        )
        db.session.add(user)
    
    db.session.commit()
    print(f"{num_users} dummy users added.")

# Function to add dummy images
def add_dummy_images(num_images=10):
    for _ in range(num_images):
        image = Image(
            image_path=faker.file_path(extension='jpg')
        )
        db.session.add(image)
    
    db.session.commit()
    print(f"{num_images} dummy images added.")

# Function to add dummy reactions
def add_dummy_reactions(num_reactions=50):
    users = User.query.all()
    images = Image.query.all()
    
    for _ in range(num_reactions):
        reaction = Reaction(
            user_id=random.choice(users).id,
            image_id=random.choice(images).id,
            reaction_value=random.choice([True, False])
        )
        db.session.add(reaction)
    
    db.session.commit()
    print(f"{num_reactions} dummy reactions added.")

def add_dummy_user_matches(num_matches=10):
    users = User.query.all()

    for _ in range(num_matches):
        user1 = random.choice(users)
        user2 = random.choice(users)
        while user2 == user1:
            user2 = random.choice(users)

        match = UserMatch(
            user1=user1,
            user2=user2,
            match_score=random.uniform(0, 1)
        )
        db.session.add(match)
    
    db.session.commit()
    print(f"{num_matches} dummy user matches added.")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        add_dummy_users(10)  # Adjust the number of users as needed
        add_dummy_images(10)  # Adjust the number of images as needed
        add_dummy_reactions(50)  # Adjust the number of reactions as needed
        add_dummy_user_matches(10) #Adjust the number of user matches as needed
