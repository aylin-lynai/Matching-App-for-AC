from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, flask_app as app, User, Image, Reaction

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            name = data['name']
            email = data['email']
            password = generate_password_hash(data['password'], method='pbkdf2:sha256')
            new_user = User(name=name, email=email, password=password)
            db.session.add(new_user)
            db.session.commit()
            return jsonify({"message": "User registered successfully"}), 201
        return jsonify({"error": "Request must be JSON"}), 415
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            email = data['email']
            password = data['password']
            user = User.query.filter_by(email=email).first()
            if user and check_password_hash(user.password, password):
                login_user(user)
                return jsonify({"message": "Login successful", "redirect": "/"})
            return jsonify({"error": "Invalid credentials"}), 401
        return jsonify({"error": "Request must be JSON"}), 415
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/admin/users')
@login_required
def admin_users():
    if current_user.is_authenticated and current_user.is_admin:
        users = User.query.all()
        return render_template('admin_users.html', users=users)
    else:
        return "Unauthorized", 403



@app.route('/users', methods=['POST'])
def add_user():
    if request.is_json:
        data = request.get_json()
        name = data['name']
        email = data['email']
        user = User(name=name, email=email)
        db.session.add(user)
        db.session.commit()
        return jsonify({"id": user.id, "name": user.name, "email": user.email}), 201
    return jsonify({"error": "Request must be JSON"}), 415

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{"id": user.id, "name": user.name, "email": user.email} for user in users])

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify({"id": user.id, "name": user.name, "email": user.email})

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
    return render_template('home.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5003)
