from datetime import datetime, timedelta
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models import Slot

calendar_view_bp = Blueprint("calendar_view_bp", __name__)

SLOT_TIME_RANGES = {
    "9-5": (datetime.strptime("09:00", "%H:%M").time(), datetime.strptime("17:00", "%H:%M").time()),
    "10-6": (datetime.strptime("10:00", "%H:%M").time(), datetime.strptime("18:00", "%H:%M").time()),
    "11-7": (datetime.strptime("11:00", "%H:%M").time(), datetime.strptime("19:00", "%H:%M").time()),
    "12-8": (datetime.strptime("12:00", "%H:%M").time(), datetime.strptime("20:00", "%H:%M").time()),
}


def get_slot_range_key(start, end):
    for key, (s, e) in SLOT_TIME_RANGES.items():
        if start == s and end == e:
            return key
    return None


@calendar_view_bp.route("/calendar-view")
@login_required
def calendar_view():
    user_id = current_user.id
    today = datetime.today().date()
    next_seven_days = [today + timedelta(days=i) for i in range(7)]

    slots = Slot.query.filter(Slot.date.in_(
        [d for d in next_seven_days])).all()

    slot_map = {d.strftime("%Y-%m-%d"): [] for d in next_seven_days}
    for slot in slots:
        slot_map[slot.date.strftime("%Y-%m-%d")].append(slot)

    return render_template(
        "calendar_view.html",
        slot_map=slot_map,
        user_id=user_id,
        days=next_seven_days,
        SLOT_TIME_RANGES=SLOT_TIME_RANGES,
        get_slot_range_key=get_slot_range_key
    )


@calendar_view_bp.route("/book-from-calendar", methods=["POST"])
@login_required
def book_from_calendar():
    from app.models import Branch, Section, Booking, db
    user_id = current_user.id
    date = request.form["date"]
    slot_range = request.form["slot_range"]
    branch = request.form["branch"]
    section = request.form["section"]

    start_time, end_time = SLOT_TIME_RANGES.get(slot_range, (None, None))
    if not start_time or not end_time:
        flash("Invalid slot selected. Please try again.", "danger")
        return redirect(url_for("calendar_view_bp.calendar_view"))

    branch_obj = Branch.query.filter_by(name=branch).first()
    section_obj = Section.query.filter_by(name=section).first()
    if not branch_obj or not section_obj:
        flash("Invalid branch or section.", "danger")
        return redirect(url_for("calendar_view_bp.calendar_view"))

    existing_booking = (
        db.session.query(Booking)
        .join(Slot)
        .filter(Booking.user_id == user_id, Slot.date == date, Slot.branch_id == branch_obj.id)
        .first()
    )
    if existing_booking:
        flash(
            f"You’ve already booked a slot in {branch} on {date}.", "warning")
        return redirect(url_for("calendar_view_bp.calendar_view"))

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
        flash("Slot no longer available or mismatched.", "danger")

    return redirect(url_for("calendar_view_bp.calendar_view"))
