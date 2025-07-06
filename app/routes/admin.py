from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.models import db, User, Slot, Branch, Section, Booking
from app.utils.helpers import admin_required
from sqlalchemy.orm import joinedload

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
    users = []
    branches = []
    sections = []
    bookings = []
    unbooked_slots = []

    # --- Users Tab Search ---
    if tab == 'users':
        user_q = request.args.get('q', '').strip().lower()
        users_query = User.query
        if user_q:
            users_query = users_query.filter(
                (User.name.ilike(f"%{user_q}%")) | (
                    User.email.ilike(f"%{user_q}%"))
            )
        users = users_query.order_by(User.name).all()

    # --- Slots Tab Filters ---
    elif tab == 'slots':
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

    # --- Bookings Tab Filters ---
    elif tab == 'bookings':
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

    # --- Other Tabs (default) ---
    elif tab == 'branches':
        branches = Branch.query.order_by(Branch.name).all()
    elif tab == 'sections':
        sections = Section.query.order_by(Section.name).all()

    return render_template(
        'admin/dashboard.html',
        tab=tab,
        slots=slots,
        users=users,
        branches=branches,
        sections=sections,
        bookings=bookings,
        unbooked_slots=unbooked_slots,
        all_slots=all_slots,
        all_users=all_users,
        all_branches=all_branches,
        all_sections=all_sections,
        all_bookings=all_bookings
    )

# --------- Manage Users Actions ----------


@admin_bp.route('/user/promote/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def promote_user(user_id):
    user = User.query.get_or_404(user_id)
    user.is_admin = True
    user.role = "admin"
    db.session.commit()
    flash("User promoted to admin!", "success")
    return redirect(url_for('admin.dashboard', tab='users'))


@admin_bp.route('/user/delete/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash("User deleted!", "info")
    return redirect(url_for('admin.dashboard', tab='users'))

# --------- Manage Branches Actions ----------


@admin_bp.route('/branch/create', methods=['POST'])
@login_required
@admin_required
def create_branch():
    name = request.form['name']
    address = request.form['address']
    city = request.form['city']
    branch = Branch(name=name, address=address, city=city)
    db.session.add(branch)
    db.session.commit()
    flash("Branch created!", "success")
    return redirect(url_for('admin.dashboard', tab='branches'))


@admin_bp.route('/branch/delete/<int:branch_id>', methods=['POST'])
@login_required
@admin_required
def delete_branch(branch_id):
    branch = Branch.query.get_or_404(branch_id)
    db.session.delete(branch)
    db.session.commit()
    flash("Branch deleted!", "info")
    return redirect(url_for('admin.dashboard', tab='branches'))

# --------- Manage Sections Actions ----------


@admin_bp.route('/section/create', methods=['POST'])
@login_required
@admin_required
def create_section():
    name = request.form['name']
    type_ = request.form['type']
    section = Section(name=name, type=type_)
    db.session.add(section)
    db.session.commit()
    flash("Section created!", "success")
    return redirect(url_for('admin.dashboard', tab='sections'))


@admin_bp.route('/section/delete/<int:section_id>', methods=['POST'])
@login_required
@admin_required
def delete_section(section_id):
    section = Section.query.get_or_404(section_id)
    db.session.delete(section)
    db.session.commit()
    flash("Section deleted!", "info")
    return redirect(url_for('admin.dashboard', tab='sections'))
