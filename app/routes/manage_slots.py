from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from app.models import db, Slot, Branch, Section
from app.utils.helpers import admin_required
from datetime import date

manage_slots_bp = Blueprint(
    'manage_slots_bp', __name__, url_prefix='/admin/slots')

# Define this once at the top so it's accessible everywhere in the file.
SLOT_TIME_RANGES = {
    "9-5": ("09:00", "17:00"),
    "10-6": ("10:00", "18:00"),
    "11-7": ("11:00", "19:00"),
    "12-8": ("12:00", "20:00")
}


# @manage_slots_bp.route('/')
# @login_required
# @admin_required
# def list_slots():
#     slots = Slot.query.order_by(Slot.date, Slot.start_time).all()
#     branches = Branch.query.all()
#     sections = Section.query.all()
#     return render_template('admin/manage_slots.html', slots=slots, branches=branches, sections=sections)
@manage_slots_bp.route('/')
@login_required
@admin_required
def list_slots():
    slots = Slot.query.order_by(Slot.date, Slot.start_time).all()
    branches = Branch.query.all()
    sections = Section.query.all()
    today = date.today()
    return render_template(
        'admin/manage_slots.html',
        slots=slots,
        branches=branches,
        sections=sections,
        today=today
    )


@manage_slots_bp.route('/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_slot():
    branches = Branch.query.all()
    sections = Section.query.all()
    if request.method == 'POST':
        date = request.form['date']
        slot_range = request.form['slot_range']
        start_time, end_time = SLOT_TIME_RANGES[slot_range]
        branch_id = request.form['branch_id']
        section_id = request.form['section_id']
        # Check for duplicate slot
        exists = Slot.query.filter_by(
            date=date,
            start_time=start_time,
            end_time=end_time,
            branch_id=branch_id,
            section_id=section_id
        ).first()
        if exists:
            flash('Slot already exists for that time/branch/section.', 'danger')
            return redirect(url_for('manage_slots_bp.create_slot'))
        slot = Slot(
            date=date,
            start_time=start_time,
            end_time=end_time,
            branch_id=branch_id,
            section_id=section_id
        )
        db.session.add(slot)
        db.session.commit()
        flash('Slot created!', 'success')
        return redirect(url_for('admin.dashboard', tab='slots'))
    return render_template('admin/create_slot.html', branches=branches, sections=sections, SLOT_TIME_RANGES=SLOT_TIME_RANGES)


@manage_slots_bp.route('/edit/<int:slot_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_slot(slot_id):
    slot = Slot.query.get_or_404(slot_id)
    branches = Branch.query.all()
    sections = Section.query.all()
    if request.method == 'POST':
        slot.date = request.form['date']
        slot_range = request.form['slot_range']
        slot.start_time, slot.end_time = SLOT_TIME_RANGES[slot_range]
        slot.branch_id = request.form['branch_id']
        slot.section_id = request.form['section_id']
        db.session.commit()
        flash('Slot updated!', 'success')
        return redirect(url_for('admin.dashboard', tab='slots'))
    return render_template('admin/edit_slot.html', slot=slot, branches=branches, sections=sections, SLOT_TIME_RANGES=SLOT_TIME_RANGES)


@manage_slots_bp.route('/delete/<int:slot_id>', methods=['POST'])
@login_required
@admin_required
def delete_slot(slot_id):
    slot = Slot.query.get_or_404(slot_id)
    if slot.bookings:
        flash("Cannot delete: This slot has existing bookings.", "danger")
        return redirect(url_for('manage_slots_bp.list_slots'))
    db.session.delete(slot)
    db.session.commit()
    flash('Slot deleted!', 'info')
    return redirect(url_for('admin.dashboard', tab='slots'))
