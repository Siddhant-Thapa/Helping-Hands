from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, request
from app.models import db, Booking, Feedback, Slot
from flask_login import login_required, current_user

my_bookings_bp = Blueprint("my_bookings_bp", __name__)


@my_bookings_bp.route("/my-bookings")
@login_required
def my_bookings():
    user_id = current_user.id
    today = datetime.today().date()

    bookings = Booking.query.filter_by(
        user_id=user_id
    ).join(Slot).order_by(Slot.date).all()

    past, upcoming = [], []

    for booking in bookings:
        slot = booking.slot
        slot_date = slot.date
        feedback = Feedback.query.filter_by(
            booking_id=booking.id, user_id=user_id
        ).first()
        slot.feedback_given = bool(feedback)
        slot.booking_id = booking.id  # Useful for feedback

        if slot_date < today:
            past.append(slot)
        else:
            upcoming.append(slot)

    return render_template("my_bookings.html", upcoming=upcoming, past=past)


@my_bookings_bp.route("/cancel-booking/<int:booking_id>", methods=["POST"])
@login_required
def cancel_booking(booking_id):
    user_id = current_user.id
    booking = Booking.query.get(booking_id)

    if booking and booking.user_id == user_id:
        db.session.delete(booking)
        db.session.commit()
        flash("Your booking has been cancelled.", "info")
    else:
        flash("You are not authorized to cancel this booking.", "danger")

    return redirect(url_for("my_bookings_bp.my_bookings"))
