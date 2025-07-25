from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.models import db, Section
from app.utils.helpers import admin_required
from datetime import datetime

manage_sections_bp = Blueprint(
    'manage_sections_bp', __name__, url_prefix='/admin/sections')


@manage_sections_bp.route('/', methods=['GET', 'POST'])
@login_required
@admin_required
def sections_dashboard():
    if request.method == 'POST':
        name = request.form['name']
        type_ = request.form['type']
        section = Section(name=name, type=type_)
        db.session.add(section)
        db.session.commit()
        flash("Section created!", "success")
        return redirect(url_for('manage_sections_bp.sections_dashboard'))

    sections = Section.query.order_by(Section.name).all()
    return render_template('admin/sections_dashboard.html', sections=sections)


@manage_sections_bp.route('/toggle/<int:section_id>', methods=['POST'])
@login_required
@admin_required
def toggle_section(section_id):
    section = Section.query.get_or_404(section_id)

    if section.is_active:
        # Deactivating section
        section.is_active = False
        section.deactivated_at = datetime.utcnow()
        flash(f"Section '{section.name}' has been deactivated.", "info")
    else:
        # Activating section
        section.is_active = True
        section.deactivated_at = None
        flash(f"Section '{section.name}' has been activated.", "success")

    db.session.commit()
    return redirect(url_for('manage_sections_bp.sections_dashboard'))
