from werkzeug.security import generate_password_hash, check_password_hash
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, current_app
import os
from werkzeug.utils import secure_filename
from app.models import db, User
from app.utils.helpers import allowed_file  # If you have this helper

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

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Email already registered.", "danger")
            return redirect(url_for('auth_bp.register'))

        user = User(name=name, email=email, password_hash=password, role=role)
        db.session.add(user)
        db.session.commit()
        flash("Registered successfully!", "success")
        return redirect(url_for('auth_bp.login'))

    return render_template('register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = str(user.id)
            session['user_name'] = user.name
            session['user_role'] = user.role
            flash("Welcome " + user.name, "success")
            return redirect(url_for('auth_bp.dashboard'))
        else:
            flash("Invalid credentials.", "danger")

    return render_template('login.html')


@auth_bp.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('auth_bp.login'))

    user = User.query.get(int(session['user_id']))
    return render_template("dashboard.html", user=user)


@auth_bp.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user_id' not in session:
        return redirect(url_for('auth_bp.login'))

    user = User.query.get(int(session['user_id']))

    if request.method == 'POST':
        updated_name = request.form['name']
        updated_role = request.form['role']

        user.name = updated_name
        user.role = updated_role

        # Handle image upload
        if 'photo' in request.files:
            file = request.files['photo']
            if file and file.filename != "" and allowed_file(file.filename):
                filename = secure_filename(
                    str(user.id) + "_" + file.filename)
                file_path = os.path.join(
                    current_app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                user.photo = filename

        db.session.commit()
        session['user_name'] = updated_name
        session['user_role'] = updated_role
        flash("Profile updated successfully!", "success")
        return redirect(url_for('auth_bp.profile'))

    return render_template("profile.html", user=user)


@auth_bp.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully.", "info")
    return redirect(url_for('auth_bp.home'))
