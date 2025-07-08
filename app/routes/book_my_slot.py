from datetime import time
from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import db, Slot, Booking, Branch, Section
from flask_login import login_required, current_user

book_my_slot_bp = Blueprint("book_my_slot_bp", __name__)

SLOT_TIME_RANGES = {
    "9-5": (time(9, 0), time(17, 0)),
    "10-6": (time(10, 0), time(18, 0)),
    "11-7": (time(11, 0), time(19, 0)),
    "12-8": (time(12, 0), time(20, 0)),
}

BANGALORE_BRANCHES = [
    "Indiranagar", "Whitefield", "Malleshwaram", "Koramangala", "HSR Layout"
]

STORE_SECTIONS = [
    "Electronics", "Clothing", "Shoes", "Furniture", "Grocery (Non-Veg)", "Veg"
]


@book_my_slot_bp.route("/book-slot", methods=["GET", "POST"])
@login_required
def book_slot():
    user_id = current_user.id

    if request.method == "POST":
        date = request.form["date"]
        slot_range = request.form["slot_range"]
        branch = request.form["branch"]
        section = request.form["section"]

        start_time, end_time = SLOT_TIME_RANGES.get(slot_range, (None, None))
        if not start_time or not end_time:
            flash("Invalid slot selected.", "danger")
            return redirect(url_for("book_my_slot_bp.book_slot"))

        branch_obj = Branch.query.filter_by(name=branch).first()
        section_obj = Section.query.filter_by(name=section).first()

        if not branch_obj or not section_obj:
            flash("Invalid branch or section.", "danger")
            return redirect(url_for("book_my_slot_bp.book_slot"))

        slot = Slot.query.filter_by(
            date=date,
            start_time=start_time,
            end_time=end_time,
            branch_id=branch_obj.id,
            section_id=section_obj.id
        ).first()

        if slot:
            booking = Booking.query.filter_by(slot_id=slot.id).first()
            if booking:
                flash("This slot is already booked!", "danger")
            else:
                new_booking = Booking(slot_id=slot.id, user_id=user_id)
                db.session.add(new_booking)
                db.session.commit()
                flash("Slot booked successfully!", "success")
        else:
            slot = Slot(
                date=date,
                start_time=start_time,
                end_time=end_time,
                branch_id=branch_obj.id,
                section_id=section_obj.id
            )
            db.session.add(slot)
            db.session.commit()
            new_booking = Booking(slot_id=slot.id, user_id=user_id)
            db.session.add(new_booking)
            db.session.commit()
            flash("Slot created and booked!", "success")

        return redirect(url_for("book_my_slot_bp.book_slot"))

    all_slots = Slot.query.all()
    return render_template("book_slot.html", slots=all_slots,
                           branches=BANGALORE_BRANCHES,
                           sections=STORE_SECTIONS)
