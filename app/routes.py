import os
from flask import request, jsonify, send_from_directory
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from marshmallow import ValidationError

from app import app, bcrypt, db
from app.models import Post, User
from app.schemas import UserSchema, LoginSchema, PostSchema
import secrets
from werkzeug.utils import secure_filename

user_schema = UserSchema()
login_schema = LoginSchema()
post_schema = PostSchema()
posts_schema = PostSchema(many=True)

FRONTEND_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'frontend')

@app.route("/")
def index():
    return send_from_directory(FRONTEND_FOLDER, 'index.html')

@app.route("/registration", methods=['POST'])
def registration():
    try:
        data = user_schema.load(request.get_json() or {})
    except ValidationError as err:
        return jsonify(err.messages), 400

    if User.query.filter_by(email=data['email']).first():
        return jsonify({"message": "Email already exists"}), 400
    if User.query.filter_by(username=data['username']).first():
        return jsonify({"message": "This username already exists"}), 400

    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    user = User(username=data['username'],
                email=data['email'],
                password=hashed_password)
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User created successfully", "user": user_schema.dump(user)}), 201

@app.route("/SignIn", methods=['POST'])
def SignIn():
    try:
        data = login_schema.load(request.get_json() or {})
    except ValidationError as err:
        return jsonify(err.messages), 400

    user = User.query.filter_by(email=data['email']).first()
    if user and bcrypt.check_password_hash(user.password, data['password']):
        access_token = create_access_token(identity=str(user.id))
        return jsonify({"access_token": access_token, "user_id": user.id}), 200

    return jsonify({"message": "Invalid email or password"}), 401



def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static', 'profile_pics', picture_fn)
    form_picture.save(picture_path)
    return picture_fn

@app.route("/user/me", methods=['GET', 'PUT'])
@jwt_required()
def get_user_profile():
    user_id = get_jwt_identity()
    user = User.query.get(int(user_id))
    if not user:
        return jsonify({"message": "User not found"}), 404
        
    if request.method == 'PUT':
        data = request.get_json() or {}
        if 'Bio' in data:
            user.Bio = data['Bio']
            db.session.commit()
            
    return jsonify({"id": user.id, "username": user.username, "email": user.email, "Bio": user.Bio, "image_file": user.image_file}), 200

@app.route("/user/profile_picture", methods=['POST'])
@jwt_required()
def upload_profile_picture():
    user_id = get_jwt_identity()
    user = User.query.get(int(user_id))
    if not user:
        return jsonify({"message": "User not found"}), 404

    if 'profile_picture' not in request.files:
        return jsonify({"message": "No picture uploaded"}), 400

    pic = request.files['profile_picture']
    if pic.filename == '':
        return jsonify({"message": "No picture selected"}), 400

    if pic:
        picture_file = save_picture(pic)
        user.image_file = picture_file
        db.session.commit()
        return jsonify({"message": "Profile picture updated", "image_file": picture_file}), 200

@app.route("/archive", methods=['GET'])
def archive():
    posts = Post.query.all()
    return jsonify({"posts": posts_schema.dump(posts)}), 200

@app.route("/post/<int:post_id>", methods=['GET'])
def get_post(post_id):
    post = Post.query.get_or_404(post_id)
    return jsonify({"post": post_schema.dump(post)}), 200

@app.route("/post/new", methods=['POST'])
@jwt_required()
def new_post():
    try:
        data = post_schema.load(request.get_json() or {})
    except ValidationError as err:
        return jsonify(err.messages), 400

    current_user_id = get_jwt_identity()
    user = User.query.get(int(current_user_id))
    
    post = Post(
        title=data['title'],
        content=data['content'],
        author=user)
    db.session.add(post)
    db.session.commit()
    
    return jsonify({"message": "Post created successfully", "post": post_schema.dump(post)}), 201

@app.route("/post/<int:post_id>", methods=['DELETE'])
@jwt_required()
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    current_user_id = get_jwt_identity()
    
    # Optional: check if the user is the author of the post
    if str(post.user_id) != str(current_user_id):
        return jsonify({"message": "You are not authorized to delete this post. Only the author can delete the post"}), 403

    db.session.delete(post)
    db.session.commit()
    return jsonify({"message": "Post deleted successfully"}), 200

@app.route("/post/<int:post_id>", methods=['PUT'])
@jwt_required()
def Edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    current_user_id = get_jwt_identity()

    if str(post.user_id) != str(current_user_id):
        return jsonify({"message": "You are not authorized to edit this post. Only the author can edit it."}), 403
    
    try:
        data = post_schema.load(request.get_json() or {})
    except ValidationError as err:
        return jsonify(err.messages), 400
        
    # Update existing post fields
    post.title = data['title']
    post.content = data['content']
    
    db.session.commit()
    
    return jsonify({"message": "Post updated successfully", "post": post_schema.dump(post)}), 200

@app.route("/<path:filename>")
def serve_frontend(filename):
    return send_from_directory(FRONTEND_FOLDER, filename)
