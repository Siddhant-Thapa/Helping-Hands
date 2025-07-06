from datetime import datetime, timedelta, time
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from app.models import db, Slot, Booking, Feedback, Branch, Section, User

# --- Flask-Login imports ---
from flask_login import login_required, current_user

slot_bp = Blueprint("slot_bp", __name__)

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


@slot_bp.route("/book-slot", methods=["GET", "POST"])
@login_required  # --- Use Flask-Login's login_required ---
def book_slot():
    # Use current_user.id instead of session['user_id']
    user_id = current_user.id

    if request.method == "POST":
        date = request.form["date"]
        slot_range = request.form["slot_range"]  # e.g., "9-5"
        branch = request.form["branch"]
        section = request.form["section"]

        start_time, end_time = SLOT_TIME_RANGES.get(slot_range, (None, None))
        if not start_time or not end_time:
            flash("Invalid slot selected.", "danger")
            return redirect(url_for("slot_bp.book_slot"))

        branch_obj = Branch.query.filter_by(name=branch).first()
        section_obj = Section.query.filter_by(name=section).first()

        if not branch_obj or not section_obj:
            flash("Invalid branch or section.", "danger")
            return redirect(url_for("slot_bp.book_slot"))

        # Check if this slot already exists
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
            # Create new slot and book it
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

        return redirect(url_for("slot_bp.book_slot"))

    all_slots = Slot.query.all()
    return render_template("book_slot.html", slots=all_slots,
                           branches=BANGALORE_BRANCHES,
                           sections=STORE_SECTIONS)


@slot_bp.route("/calendar-view")
@login_required  # --- Use Flask-Login's login_required ---
def calendar_view():
    user_id = current_user.id

    today = datetime.today().date()
    next_seven_days = [today + timedelta(days=i) for i in range(7)]

    slots = Slot.query.filter(Slot.date.in_(
        [d for d in next_seven_days])).all()

    slot_map = {d.strftime("%Y-%m-%d"): [] for d in next_seven_days}
    for slot in slots:
        slot_map[slot.date.strftime("%Y-%m-%d")].append(slot)

    return render_template("calendar_view.html", slot_map=slot_map, user_id=user_id, days=next_seven_days, SLOT_TIME_RANGES=SLOT_TIME_RANGES)


@slot_bp.route("/book-from-calendar", methods=["POST"])
@login_required  # --- Use Flask-Login's login_required ---
def book_from_calendar():
    user_id = current_user.id
    date = request.form["date"]
    slot_range = request.form["slot_range"]
    branch = request.form["branch"]
    section = request.form["section"]

    start_time, end_time = SLOT_TIME_RANGES.get(slot_range, (None, None))
    if not start_time or not end_time:
        flash("Invalid slot selected.", "danger")
        return redirect(url_for("slot_bp.calendar_view"))

    branch_obj = Branch.query.filter_by(name=branch).first()
    section_obj = Section.query.filter_by(name=section).first()
    if not branch_obj or not section_obj:
        flash("Invalid branch or section.", "danger")
        return redirect(url_for("slot_bp.calendar_view"))

    # Prevent multiple bookings on same branch/date
    existing_booking = (
        db.session.query(Booking)
        .join(Slot)
        .filter(Booking.user_id == user_id,
                Slot.date == date,
                Slot.branch_id == branch_obj.id)
        .first()
    )
    if existing_booking:
        flash(
            f"You’ve already booked a slot in {branch} on {date}.", "warning")
        return redirect(url_for("slot_bp.calendar_view"))

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
        # Create slot and booking
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

    return redirect(url_for("slot_bp.calendar_view"))


@slot_bp.route("/my-bookings")
@login_required  # --- Use Flask-Login's login_required ---
def my_bookings():
    user_id = current_user.id
    today = datetime.today().date()

    bookings = Booking.query.filter_by(
        user_id=user_id).join(Slot).order_by(Slot.date).all()

    past, upcoming = [], []

    for booking in bookings:
        slot = booking.slot
        slot_date = slot.date
        feedback = Feedback.query.filter_by(
            booking_id=booking.id, user_id=user_id).first()
        slot.feedback_given = bool(feedback)
        slot.booking_id = booking.id  # Useful for feedback

        if slot_date < today:
            past.append(slot)
        else:
            upcoming.append(slot)

    return render_template("my_bookings.html", upcoming=upcoming, past=past)


@slot_bp.route("/cancel-booking/<int:booking_id>", methods=["POST"])
@login_required  # --- Use Flask-Login's login_required ---
def cancel_booking(booking_id):
    user_id = current_user.id
    booking = Booking.query.get(booking_id)

    if booking and booking.user_id == user_id:
        db.session.delete(booking)
        db.session.commit()
        flash("Your booking has been cancelled.", "info")
    else:
        flash("You are not authorized to cancel this booking.", "danger")

    return redirect(url_for("slot_bp.my_bookings"))


@slot_bp.route("/create-slot", methods=["GET", "POST"])
@login_required  # --- Use Flask-Login's login_required ---
def create_slot():
    # 🚫 Temporary block everyone from accessing this route
    flash("🚫 This feature is restricted to admins.", "danger")
    return redirect(url_for("slot_bp.calendar_view"))


@slot_bp.route("/dashboard")
@login_required  # --- Use Flask-Login's login_required ---
def dashboard():
    return render_template("dashboard.html")
