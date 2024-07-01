from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from models import db, flask_app as app, User, Image, Reaction
from happiness_detector import analyze_image
from sqlalchemy.exc import IntegrityError
import traceback
import dummy_data

app.secret_key = 'supersecretkey' 
image_list = ['1.jpg', '2.jpg', '3.jpg', '4.jpg', '5.jpg', '6.jpg', '7.jpg', '8.jpg', '9.jpg', '10.jpg', 
              '11.jpg', '12.jpg', '13.jpg', '14.jpg', '15.jpg', '16.jpg', '17.jpg', '18.jpg', '19.jpg']

@app.route('/generate-dummy-data', methods=['POST'])
def generate_dummy_data():
    num_users = request.json.get('num_users', 10)
    num_images = request.json.get('num_images', 10)
    num_reactions = request.json.get('num_reactions', 50)
    num_matches = request.json.get('num_matches', 10)
    
    dummy_data.add_dummy_users(num_users)
    dummy_data.add_dummy_images(num_images)
    dummy_data.add_dummy_reactions(num_reactions)
    dummy_data.add_dummy_reactions(num_matches)
    
    return jsonify({"message": "Dummy data generated"}), 201

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        if request.is_json:
            try:
                data = request.get_json()
                print("Data received: ", data)  # Debug print
                username = data['username']
                email = data['email']
                new_user = User(username=username, email=email)
                db.session.add(new_user)
                db.session.commit()
                return jsonify({"message": "User registered successfully"}), 201
            except IntegrityError as e:
                db.session.rollback()
                print("Integrity Error: ", e)  # More detailed error print
                return jsonify({"error": "This email is already registered."}), 409
            except Exception as e:
                db.session.rollback()
                print("Exception Error: ", e)  # Print full error message
                print("Traceback: ", traceback.format_exc())  # Print traceback
                return jsonify({"error": str(e)}), 500
        else:
            return jsonify({"error": "Request must be JSON"}), 415

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            username = data['username']
            email = data['email']
            user = User.query.filter_by(username=username, email=email).first()
            if user:
                login_user(user)
                return jsonify({"message": "Login successful", "redirect": "/cameratest"})
            else:
                return jsonify({"error": "Invalid credentials"}), 401
        else:
            return jsonify({"error": "Request must be JSON"}), 415


@app.route('/cameratest')
# @login_required
def camera_test():
    return render_template('cameratest.html')

@app.route('/test')
# @login_required
def test():
    return render_template('test.html')

@app.route('/matchpage')
# @login_required
def match_page():
    return render_template('matchpage.html')

@app.route('/resultpage')
# @login_required
def result_page():
    return render_template('resultpage.html')

@app.route('/logout')
# @login_required
def logout():
    logout_user()
    return redirect(url_for('startpage'))

@app.route('/admin/users')
def admin_users():
    users = db.session.query(User.id, User.username, User.email).all()
    return render_template('admin_users.html', users=users)

@app.route('/users', methods=['POST'])
def add_user():
    if request.is_json:
        data = request.get_json()
        username = data['username']
        email = data['email']
        user = User(username=username, email=email)
        db.session.add(user)
        db.session.commit()
        return jsonify({"id": user.id, "username": user.username, "email": user.email}), 201
    return jsonify({"error": "Request must be JSON"}), 415

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{"id": user.id, "username": user.username, "email": user.email} for user in users])

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify({"id": user.id, "username": user.username, "email": user.email})

@app.route('/images', methods=['POST'])
def add_image():
    if request.is_json:
        data = request.get_json()
        image_path = data['image_path']
        image = Image(image_path=image_path)
        db.session.add(image)
        db.session.commit()
        return jsonify({"id": image.id, "path": image.image_path}), 201
    return jsonify({"error": "Request must be JSON"}), 415

@app.route('/images', methods=['GET'])
def get_images():
    images = Image.query.all()
    return jsonify([{"id": image.id, "path": image.image_path} for image in images])

@app.route('/images/view', methods=['GET'])
def view_images():
    images = Image.query.all()
    return render_template('images.html', images=images)

@app.route('/reactions', methods=['POST'])
def add_reaction():
    if request.is_json:
        data = request.get_json()
        user_id = data['user_id']
        image_id = data['image_id']
        reaction_value = data['reaction_value']
        reaction = Reaction(user_id=user_id, image_id=image_id, reaction_value=reaction_value)
        db.session.add(reaction)
        db.session.commit()
        return jsonify({"id": reaction.id}), 201
    return jsonify({"error": "Request must be JSON"}), 415

@app.route('/reactions', methods=['GET'])
def get_reactions():
    reactions = Reaction.query.all()
    return jsonify([
        {"id": reaction.id, "user_id": reaction.user_id, "image_id": reaction.image_id, "reaction_value": reaction.reaction_value} 
        for reaction in reactions
    ])

@app.route('/reactions/view', methods=['GET'])
def view_reactions():
    reactions = Reaction.query.all()
    return render_template('reactions.html', reactions=reactions)

@app.route('/users')
def list_users():
    users = User.query.all()
    return render_template('users.html', users=users)

@app.route('/')
def home():
    return render_template('startpage.html')

@app.route('/analyze_emotions', methods=['POST'])
def analyze_emotions():
    data = request.json
    image_data = data['image_data']
    analysis_result = analyze_image(image_data)
    return jsonify(analysis_result)

@app.route('/capture_reaction', methods=['POST'])
def capture_reaction():
    data = request.json
    user_id = current_user.id
    happiness_score = data['happiness_score']
    current_image_index = data['current_image_index']

    reaction = Reaction(user_id=user_id, image_id=current_image_index, happiness_score=happiness_score)
    db.session.add(reaction)
    db.session.commit()

    return jsonify({"dominant_emotion": None, "happiness_score": happiness_score}), 200

@app.route('/reacted_images', methods=['GET'])
def get_reacted_images():
    user_id = current_user.id
    reacted_images = Reaction.query.filter_by(user_id=user_id).all()
    reacted_image_ids = [reaction.image_id for reaction in reacted_images]
    return jsonify(reacted_image_ids)

@app.route('/ranked_users', methods=['GET'])
@login_required
def get_ranked_users():
    user_id = current_user.id
    ranked_users = rank_users(user_id)
    return jsonify(ranked_users)

def calculate_similarity(user1, user2):
    reactions1 = {reaction.image_id: reaction.happiness_score for reaction in user1.reactions}
    reactions2 = {reaction.image_id: reaction.happiness_score for reaction in user2.reactions}

    common_reactions = set(reactions1.keys()) & set(reactions2.keys())
    if not common_reactions:
        return 0

    similarity = sum(reactions1[image_id] == reactions2[image_id] for image_id in common_reactions) / len(common_reactions)
    return similarity

def rank_users(user_id):
    user = User.query.get(user_id)
    users = User.query.all()
    similarities = [(other_user, calculate_similarity(user, other_user)) for other_user in users if user != other_user]
    similarities.sort(key=lambda x: x[1], reverse=True)

    ranked_users = [{"username": other_user.username, "email": other_user.email, "similarity": similarity} for other_user, similarity in similarities]
    return ranked_users


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5003)
