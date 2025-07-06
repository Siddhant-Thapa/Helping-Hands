from flask import Blueprint, render_template, request
from flask_login import login_required
from app.models import db, Feedback, Booking, Slot, Branch, Section, User
from app.utils.helpers import admin_required

manage_feedback_bp = Blueprint(
    'manage_feedback_bp', __name__, url_prefix='/admin/feedback')


@manage_feedback_bp.route('/')
@login_required
@admin_required
def feedback_dashboard():
    # Filters from query params
    user_query = request.args.get('user', '').strip().lower()
    branch_query = request.args.get('branch', '')
    section_query = request.args.get('section', '')
    date_query = request.args.get('date', '')
    min_rating = request.args.get('min_rating', '')

    # EXPLICIT joins for SQLAlchemy
    query = (Feedback.query
             .join(Booking, Feedback.booking_id == Booking.id)
             .join(Slot, Booking.slot_id == Slot.id)
             .join(Branch, Slot.branch_id == Branch.id)
             .join(Section, Slot.section_id == Section.id)
             .join(User, Feedback.user_id == User.id)
             )

    if user_query:
        query = query.filter((User.name.ilike(f"%{user_query}%")) | (
            User.email.ilike(f"%{user_query}%")))
    if branch_query:
        query = query.filter(Branch.name == branch_query)
    if section_query:
        query = query.filter(Section.name == section_query)
    if date_query:
        query = query.filter(Slot.date == date_query)
    if min_rating:
        query = query.filter(Feedback.rating <= int(min_rating))
    feedbacks = query.order_by(Feedback.submitted_at.desc()).all()

    # For filter dropdowns
    all_branches = Branch.query.order_by(Branch.name).all()
    all_sections = Section.query.order_by(Section.name).all()
    all_users = User.query.order_by(User.name).all()

    return render_template(
        'admin/feedback_dashboard.html',
        feedbacks=feedbacks,
        all_branches=all_branches,
        all_sections=all_sections,
        all_users=all_users
    )
