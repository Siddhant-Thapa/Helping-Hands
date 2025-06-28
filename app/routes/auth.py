from werkzeug.security import generate_password_hash, check_password_hash
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import os
from app.utils.helpers import allowed_file

from werkzeug.utils import secure_filename
from app import mongo
from app import create_app
from flask import current_app


auth_bp = Blueprint('auth_bp', __name__)


@auth_bp.route('/')
def home():
    return render_template("home.html")


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])
        role = request.form['role']

        existing_user = mongo.db.users.find_one({"email": email})
        if existing_user:
            flash("Email already registered.", "danger")
            return redirect(url_for('auth_bp.register'))

        mongo.db.users.insert_one({
            "name": name,
            "email": email,
            "password": password,
            "role": role
        })
        flash("Registered successfully!", "success")
        return redirect(url_for('auth_bp.login'))

    return render_template('register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = mongo.db.users.find_one({"email": email})
        if user and check_password_hash(user['password'], password):
            session['user_id'] = str(user['_id'])
            session['user_name'] = user['name']
            session['user_role'] = user['role']
            flash("Welcome " + user['name'], "success")
            return redirect(url_for('auth_bp.dashboard'))
        else:
            flash("Invalid credentials.", "danger")

    return render_template('login.html')


@auth_bp.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('auth_bp.login'))

    from bson.objectid import ObjectId
    user = mongo.db.users.find_one({"_id": ObjectId(session['user_id'])})
    return render_template("dashboard.html", user=user)


@auth_bp.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user_id' not in session:
        return redirect(url_for('auth_bp.login'))

    from bson.objectid import ObjectId
    user = mongo.db.users.find_one({'_id': ObjectId(session['user_id'])})

    if request.method == 'POST':
        updated_name = request.form['name']
        updated_role = request.form['role']

        update_data = {
            "name": updated_name,
            "role": updated_role
        }

        # Handle image upload
        if 'photo' in request.files:
            file = request.files['photo']
            if file and file.filename != "" and allowed_file(file.filename):
                filename = secure_filename(
                    session['user_id'] + "_" + file.filename)
                file_path = os.path.join(
                    current_app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                update_data["photo"] = filename

        mongo.db.users.update_one(
            {"_id": ObjectId(session['user_id'])},
            {"$set": update_data}
        )

        session['user_name'] = updated_name
        session['user_role'] = updated_role
        flash("Profile updated successfully!", "success")
        # ✅ this is your POST response
        return redirect(url_for('auth_bp.profile'))

    # ✅ this is your GET response
    return render_template("profile.html", user=user)


@auth_bp.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully.", "info")
    return redirect(url_for('auth_bp.home'))
