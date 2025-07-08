from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import db, SaleDay
from flask_login import login_required, current_user
from datetime import datetime

manage_sale_days_bp = Blueprint("manage_sale_days_bp", __name__)


@manage_sale_days_bp.route("/admin/sale-days")
@login_required
def sale_days():
    if not current_user.is_admin_user():
        flash("Not authorized", "danger")
        return redirect(url_for("user_dashboard_bp.dashboard"))
    sale_days = SaleDay.query.order_by(SaleDay.start_date).all()
    return render_template("admin/sale_days.html", sale_days=sale_days)


@manage_sale_days_bp.route("/admin/sale-days/add", methods=["POST"])
@login_required
def add_sale_day():
    if not current_user.is_admin_user():
        flash("Not authorized", "danger")
        return redirect(url_for("user_dashboard_bp.dashboard"))
    try:
        start_date_str = request.form["start_date"]
        end_date_str = request.form["end_date"]
        desc = request.form.get("description", "")
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
        if end_date < start_date:
            flash("End date must be after or equal to start date.", "warning")
        elif SaleDay.query.filter(SaleDay.start_date <= end_date, SaleDay.end_date >= start_date).first():
            flash("Sale day range overlaps with an existing sale.", "warning")
        else:
            sd = SaleDay(start_date=start_date,
                         end_date=end_date, description=desc)
            db.session.add(sd)
            db.session.commit()
            flash("Sale day range added!", "success")
    except Exception as e:
        flash("Invalid date or error: " + str(e), "danger")
    return redirect(url_for("manage_sale_days_bp.sale_days"))


@manage_sale_days_bp.route("/admin/sale-days/delete/<int:id>", methods=["POST"])
@login_required
def delete_sale_day(id):
    if not current_user.is_admin_user():
        flash("Not authorized", "danger")
        return redirect(url_for("user_dashboard_bp.dashboard"))
    sd = SaleDay.query.get(id)
    if sd:
        db.session.delete(sd)
        db.session.commit()
        flash("Sale day deleted.", "info")
    else:
        flash("Sale day not found.", "danger")
    return redirect(url_for("manage_sale_days_bp.sale_days"))
