from flask import Blueprint, render_template, request
from flask_login import login_required
from app.models import db, Slot, Branch, Section, User
from app.utils.helpers import admin_required
from datetime import date
from app.models import Booking

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    tab = request.args.get('tab', 'home')

    # For dropdowns and stats (always available)
    all_slots = Slot.query.all()
    all_users = User.query.all()
    all_branches = Branch.query.all()
    all_sections = Section.query.all()
    all_bookings = Booking.query.all()

    # Initialize table vars
    slots = []
    slots_today = []
    slots_upcoming = []
    slots_past = []
    branches = []
    sections = []
    today = date.today()

    # --- Slots Tab Filters & Grouping ---
    if tab == 'slots':
        branch_query = request.args.get('branch', '')
        section_query = request.args.get('section', '')
        date_query = request.args.get('date', '')

        query = Slot.query
        if branch_query:
            query = query.join(Slot.branch).filter(Branch.name == branch_query)
        if section_query:
            query = query.join(Slot.section).filter(
                Section.name == section_query)
        if date_query:
            query = query.filter(Slot.date == date_query)
        slots = query.order_by(Slot.date, Slot.start_time).all()

        # Group slots
        for slot in slots:
            if slot.date == today:
                slots_today.append(slot)
            elif slot.date > today:
                slots_upcoming.append(slot)
            else:
                slots_past.append(slot)

    return render_template(
        'admin/dashboard.html',
        tab=tab,
        slots=slots,
        slots_today=slots_today,
        slots_upcoming=slots_upcoming,
        slots_past=slots_past,
        branches=branches,
        sections=sections,
        all_slots=all_slots,
        all_users=all_users,
        all_branches=all_branches,
        all_sections=all_sections,
        all_bookings=all_bookings,
        today=today
    )
