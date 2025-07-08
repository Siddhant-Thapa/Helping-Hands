from flask import Blueprint, render_template
from flask_login import login_required, current_user

user_dashboard_bp = Blueprint("user_dashboard_bp", __name__)


@user_dashboard_bp.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", user=current_user)
