from flask import Blueprint, request, jsonify
from datetime import datetime
from app.models import db, Feedback, Booking
from flask_login import current_user, login_required

feedback_bp = Blueprint("feedback_bp", __name__)


@feedback_bp.route("/rate/<int:booking_id>", methods=["POST"])
@login_required
def submit_feedback(booking_id):
    user_id = current_user.id
    data = request.get_json()
    rating = int(data.get("rating", 0))
    comment = data.get("comment", "").strip()

    if rating < 1 or rating > 5:
        return jsonify({"error": "Invalid rating"}), 400

    booking = Booking.query.filter_by(id=booking_id, user_id=user_id).first()
    if not booking:
        return jsonify({"error": "Booking not found"}), 404

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
