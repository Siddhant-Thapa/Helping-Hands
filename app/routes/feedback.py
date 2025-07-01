from flask import Blueprint, request, session, jsonify
from datetime import datetime
from app.models import db, Feedback, Booking, User

feedback_bp = Blueprint("feedback_bp", __name__)


@feedback_bp.route("/rate/<int:slot_id>", methods=["POST"])
def submit_feedback(slot_id):
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    user_id = int(session["user_id"])
    data = request.get_json()
    rating = int(data.get("rating", 0))
    comment = data.get("comment", "").strip()

    if rating < 1 or rating > 5:
        return jsonify({"error": "Invalid rating"}), 400

    # Find the booking for this slot/user
    booking = Booking.query.filter_by(slot_id=slot_id, user_id=user_id).first()
    if not booking:
        return jsonify({"error": "Booking not found"}), 404

    # Check if feedback already exists
    existing = Feedback.query.filter_by(
        booking_id=booking.id, user_id=user_id).first()
    if existing:
        return jsonify({"error": "Already submitted"}), 400

    feedback = Feedback(
        booking_id=booking.id,
        user_id=user_id,
        rating=rating,
        comment=comment,
        submitted_at=datetime.utcnow()
    )
    db.session.add(feedback)
    db.session.commit()

    return jsonify({"success": True}), 200
