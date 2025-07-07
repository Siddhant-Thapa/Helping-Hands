from flask import Blueprint, render_template, request
from flask_login import login_required
from app.models import db, Slot, Branch, Section, User
from app.utils.helpers import admin_required

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

    # Initialize table vars
    slots = []
    branches = []
    sections = []

    # --- Slots Tab Filters ---
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

    return render_template(
        'admin/dashboard.html',
        tab=tab,
        slots=slots,
        branches=branches,
        sections=sections,
        all_slots=all_slots,
        all_users=all_users,
        all_branches=all_branches,
        all_sections=all_sections
    )
