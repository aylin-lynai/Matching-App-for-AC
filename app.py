from flask import Flask, request, jsonify
from models import db, flask_app as app, User, Image, Reaction

@app.route('/users', methods=['POST'])
def add_user():
    username = request.json['username']
    email = request.json['email']
    user_exists = User.query.filter_by(email=email).first()
    if user_exists:
        return jsonify({"error": "Diese E-Mail-Adresse ist bereits registriert."}), 400


    user = User(username=username, email=email)
    db.session.add(user)
    db.session.commit()
    return jsonify({"id": user.id, "username": user.username, "email": user.email}), 201

@app.route('/images', methods=['GET'])
def get_images():
    images = Image.query.all()
    return jsonify([{"id": image.id, "path": image.image_path} for image in images])

@app.route('/reactions', methods=['POST'])
def add_reaction():
    user_id = request.json['user_id']
    image_id = request.json['image_id']
    reaction_value = request.json['reaction_value']
    reaction = Reaction(user_id=user_id, image_id=image_id, reaction_value=reaction_value)
    db.session.add(reaction)
    db.session.commit()
    return jsonify({"id": reaction.id}), 201

@app.route('/')
def home():
    return "Willkommen zur Matching App!"

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
