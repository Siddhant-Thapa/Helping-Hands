from flask import Blueprint, render_template, request
from flask_login import login_required
from app.models import db, Booking, Slot, Branch, Section, User
from app.utils.helpers import admin_required
from sqlalchemy.orm import joinedload

manage_bookings_bp = Blueprint(
    'manage_bookings_bp', __name__, url_prefix='/admin/bookings')


@manage_bookings_bp.route('/', methods=['GET'])
@login_required
@admin_required
def bookings_dashboard():
    user_query = request.args.get('user', '').strip().lower()
    branch_query = request.args.get('branch', '')
    section_query = request.args.get('section', '')
    date_query = request.args.get('date', '')
    status_query = request.args.get('status', '')

    query = Booking.query.options(
        joinedload(Booking.slot),
        joinedload(Booking.user)
    )

    if user_query:
        query = query.join(User).filter(
            (User.name.ilike(f"%{user_query}%")) |
            (User.email.ilike(f"%{user_query}%"))
        )
    if branch_query:
        query = query.join(Booking.slot).join(
            Slot.branch).filter(Branch.name == branch_query)
    if section_query:
        query = query.join(Booking.slot).join(
            Slot.section).filter(Section.name == section_query)
    if date_query:
        query = query.join(Booking.slot).filter(Slot.date == date_query)
    if status_query:
        query = query.filter(Booking.status == status_query)

    bookings = query.order_by(Booking.created_at.desc()).all()

    # Unbooked slots
    unbooked_slots = Slot.query.outerjoin(Booking).filter(
        Booking.id == None).order_by(Slot.date, Slot.start_time).all()

    all_branches = Branch.query.all()
    all_sections = Section.query.all()

    return render_template(
        'admin/bookings_dashboard.html',
        bookings=bookings,
        unbooked_slots=unbooked_slots,
        all_branches=all_branches,
        all_sections=all_sections
    )
