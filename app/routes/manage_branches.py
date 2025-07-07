from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.models import db, Branch
from app.utils.helpers import admin_required

manage_branches_bp = Blueprint(
    'manage_branches_bp', __name__, url_prefix='/admin/branches')


@manage_branches_bp.route('/', methods=['GET', 'POST'])
@login_required
@admin_required
def branches_dashboard():
    if request.method == 'POST':
        # Creating a branch
        name = request.form['name']
        address = request.form['address']
        city = request.form['city']
        branch = Branch(name=name, address=address, city=city)
        db.session.add(branch)
        db.session.commit()
        flash("Branch created!", "success")
        return redirect(url_for('manage_branches_bp.branches_dashboard'))

    # GET: show all branches
    branches = Branch.query.order_by(Branch.name).all()
    return render_template('admin/branches_dashboard.html', branches=branches)


@manage_branches_bp.route('/delete/<int:branch_id>', methods=['POST'])
@login_required
@admin_required
def delete_branch(branch_id):
    branch = Branch.query.get_or_404(branch_id)
    if branch.slots:
        flash("Cannot delete: This branch is still in use by one or more slots.", "danger")
        return redirect(url_for('manage_branches_bp.branches_dashboard'))
    db.session.delete(branch)
    db.session.commit()
    flash("Branch deleted!", "info")
    return redirect(url_for('manage_branches_bp.branches_dashboard'))
