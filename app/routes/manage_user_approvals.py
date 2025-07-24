from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from app.models import db, User
from flask_login import login_required, current_user
from datetime import datetime

manage_user_approvals_bp = Blueprint(
    "manage_user_approvals_bp", __name__, url_prefix="/admin")


@manage_user_approvals_bp.route("/user-approvals")
@login_required
def user_approvals():
    """Display pending user approvals for admin"""
    if not current_user.is_admin_user():
        flash("Access denied. Admin privileges required.", "danger")
        return redirect(url_for('auth_bp.dashboard'))

    # Get users by approval status
    pending_users = User.query.filter_by(
        approval_status='pending').order_by(User.registered_at.desc()).all()
    approved_users = User.query.filter_by(approval_status='approved').order_by(
        User.registered_at.desc()).limit(10).all()
    rejected_users = User.query.filter_by(approval_status='rejected').order_by(
        User.registered_at.desc()).limit(10).all()

    return render_template(
        'admin/user_approvals.html',
        pending_users=pending_users,
        approved_users=approved_users,
        rejected_users=rejected_users
    )


@manage_user_approvals_bp.route("/approve-user/<int:user_id>", methods=["POST"])
@login_required
def approve_user(user_id):
    """Approve a pending user"""
    if not current_user.is_admin_user():
        flash("Access denied. Admin privileges required.", "danger")
        return redirect(url_for('auth_bp.dashboard'))

    user = User.query.get_or_404(user_id)

    if user.approval_status == 'pending':
        user.approval_status = 'approved'
        user.is_approved = True
        db.session.commit()
        flash(f"User {user.name} has been approved successfully!", "success")
    else:
        flash(f"User {user.name} is not in pending status.", "warning")

    return redirect(url_for('manage_user_approvals_bp.user_approvals'))


@manage_user_approvals_bp.route("/reject-user/<int:user_id>", methods=["POST"])
@login_required
def reject_user(user_id):
    """Reject a pending user"""
    if not current_user.is_admin_user():
        flash("Access denied. Admin privileges required.", "danger")
        return redirect(url_for('auth_bp.dashboard'))

    user = User.query.get_or_404(user_id)

    if user.approval_status == 'pending':
        user.approval_status = 'rejected'
        user.is_approved = False
        db.session.commit()
        flash(f"User {user.name} has been rejected.", "info")
    else:
        flash(f"User {user.name} is not in pending status.", "warning")

    return redirect(url_for('manage_user_approvals_bp.user_approvals'))


@manage_user_approvals_bp.route("/bulk-approve", methods=["POST"])
@login_required
def bulk_approve():
    """Approve multiple users at once"""
    if not current_user.is_admin_user():
        return jsonify({"error": "Access denied"}), 403

    user_ids = request.json.get('user_ids', [])

    if not user_ids:
        return jsonify({"error": "No users selected"}), 400

    try:
        users = User.query.filter(User.id.in_(
            user_ids), User.approval_status == 'pending').all()
        approved_count = 0

        for user in users:
            user.approval_status = 'approved'
            user.is_approved = True
            approved_count += 1

        db.session.commit()
        return jsonify({
            "success": True,
            "message": f"Successfully approved {approved_count} users"
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to approve users"}), 500


@manage_user_approvals_bp.route("/bulk-reject", methods=["POST"])
@login_required
def bulk_reject():
    """Reject multiple users at once"""
    if not current_user.is_admin_user():
        return jsonify({"error": "Access denied"}), 403

    user_ids = request.json.get('user_ids', [])

    if not user_ids:
        return jsonify({"error": "No users selected"}), 400

    try:
        users = User.query.filter(User.id.in_(
            user_ids), User.approval_status == 'pending').all()
        rejected_count = 0

        for user in users:
            user.approval_status = 'rejected'
            user.is_approved = False
            rejected_count += 1

        db.session.commit()
        return jsonify({
            "success": True,
            "message": f"Successfully rejected {rejected_count} users"
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to reject users"}), 500
