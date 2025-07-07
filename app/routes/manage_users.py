from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.models import db, User
from app.utils.helpers import admin_required

manage_users_bp = Blueprint(
    'manage_users_bp', __name__, url_prefix='/admin/users')


@manage_users_bp.route('/', methods=['GET'])
@login_required
@admin_required
def users_dashboard():
    q = request.args.get('q', '').strip().lower()
    users_query = User.query
    if q:
        users_query = users_query.filter(
            (User.name.ilike(f"%{q}%")) | (User.email.ilike(f"%{q}%"))
        )
    users = users_query.order_by(User.name).all()
    return render_template('admin/users_dashboard.html', users=users, q=q)


@manage_users_bp.route('/promote/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def promote_user(user_id):
    user = User.query.get_or_404(user_id)
    user.is_admin = True
    user.role = "admin"
    db.session.commit()
    flash("User promoted to admin!", "success")
    return redirect(url_for('manage_users_bp.users_dashboard'))


@manage_users_bp.route('/delete/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.bookings or user.feedbacks:
        flash("Cannot delete: This user has associated bookings or feedback.", "danger")
        return redirect(url_for('manage_users_bp.users_dashboard'))
    db.session.delete(user)
    db.session.commit()
    flash("User deleted!", "info")
    return redirect(url_for('manage_users_bp.users_dashboard'))
