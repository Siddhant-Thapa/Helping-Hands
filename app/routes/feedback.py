from flask import Blueprint, render_template, request, redirect, session, flash, url_for
from bson import ObjectId
from datetime import datetime
from app import mongo

feedback_bp = Blueprint("feedback_bp", __name__)


@feedback_bp.route("/rate/<slot_id>", methods=["POST"])
def submit_feedback(slot_id):
    if "user_id" not in session:
        return {"error": "Unauthorized"}, 401

    user_id = ObjectId(session["user_id"])
    data = request.get_json()
    rating = int(data.get("rating", 0))
    comment = data.get("comment", "").strip()

    if rating < 1 or rating > 5:
        return {"error": "Invalid rating"}, 400

    # Check if already submitted
    existing = mongo.db.feedback.find_one({
        "user_id": user_id,
        "slot_id": ObjectId(slot_id)
    })
    if existing:
        return {"error": "Already submitted"}, 400

    mongo.db.feedback.insert_one({
        "user_id": user_id,
        "slot_id": ObjectId(slot_id),
        "rating": rating,
        "comment": comment,
        "submitted_at": datetime.utcnow()
    })

    return {"success": True}, 200
