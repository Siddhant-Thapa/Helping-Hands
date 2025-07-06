from functools import wraps
from flask_login import current_user
from flask import redirect, url_for, flash
from flask import current_app


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


# helpers.py


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin_user():
            flash('Admins only!', 'danger')
            return redirect(url_for('main.home'))  # Adjust as needed
        return f(*args, **kwargs)
    return decorated_function
