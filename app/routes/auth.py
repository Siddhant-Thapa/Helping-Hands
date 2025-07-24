from werkzeug.security import generate_password_hash, check_password_hash
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, session
import os
from werkzeug.utils import secure_filename
from app.models import db, User
from app.utils.helpers import allowed_file  # If you have this helper

# --- Flask-Login imports ---
from flask_login import login_user, logout_user, login_required, current_user

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

        # Create user with pending approval status
        user = User(
            name=name,
            email=email,
            password_hash=password,
            role=role,
            is_approved=False,
            approval_status='pending'
        )
        db.session.add(user)
        db.session.commit()

        flash("Registration successful! Your account is pending admin approval. You will be notified once approved and can then login.", "info")
        return render_template('registration_pending.html', user_name=name)

    return render_template('register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        role_requested = request.form.get('role')  # 'user' or 'admin'

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password_hash, password):
            # Check if user is approved (admins bypass approval check)
            if not user.is_admin_user() and user.approval_status != 'approved':
                if user.approval_status == 'pending':
                    flash(
                        "Your account is pending admin approval. Please wait for approval before logging in.", "warning")
                elif user.approval_status == 'rejected':
                    flash(
                        "Your account has been rejected by the administrator. Please contact support.", "danger")
                else:
                    flash("Your account is not approved for login.", "danger")
                return render_template('login.html')

            if role_requested == 'admin':
                # Admin login requested
                if user.is_admin_user():
                    login_user(user)
                    session['login_role'] = 'admin'  # Track how they logged in
                    flash("Welcome Admin " + user.name, "success")
                    return redirect(url_for('admin.dashboard'))
                else:
                    flash(
                        "Access denied. You don't have administrator privileges.", "danger")
                    return render_template('login.html')
            else:
                # Regular user login
                login_user(user)
                session['login_role'] = 'user'  # Track how they logged in
                flash("Welcome " + user.name, "success")
                return redirect(url_for('user_dashboard_bp.dashboard'))
        else:
            flash("Invalid credentials.", "danger")

    return render_template('login.html')


@auth_bp.route('/dashboard')
@login_required  # --- Use Flask-Login's login_required ---
def dashboard():
    # --- Use Flask-Login's current_user ---
    user = current_user
    return render_template("dashboard.html", user=user)


@auth_bp.route('/profile', methods=['GET', 'POST'])
@login_required  # --- Use Flask-Login's login_required ---
def profile():
    user = current_user

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
        flash("Profile updated successfully!", "success")
        return redirect(url_for('auth_bp.profile'))

    return render_template("profile.html", user=user)


@auth_bp.route('/remove-profile-photo', methods=['POST'])
@login_required
def remove_profile_photo():
    user = current_user

    if user.photo:
        # Delete the physical file
        try:
            file_path = os.path.join(
                current_app.config['UPLOAD_FOLDER'], user.photo)
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception as e:
            print(f"Error deleting file: {e}")

        # Remove from database
        user.photo = None
        db.session.commit()
        flash("Profile picture removed successfully!", "success")
    else:
        flash("No profile picture to remove.", "info")

    return redirect(url_for('auth_bp.profile'))


@auth_bp.route('/logout')
@login_required  # --- Use Flask-Login's login_required ---
def logout():
    # --- Use Flask-Login to log the user out ---
    logout_user()
    flash("Logged out successfully.", "info")
    return redirect(url_for('auth_bp.home'))


@auth_bp.route('/about')
def about():
    return render_template('about.html')
