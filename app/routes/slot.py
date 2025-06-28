from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from app import mongo
from bson.objectid import ObjectId

slot_bp = Blueprint("slot_bp", __name__)

# Constants for branches and sections
BANGALORE_BRANCHES = [
    "Indiranagar", "Whitefield", "Malleshwaram", "Koramangala", "HSR Layout"
]

STORE_SECTIONS = [
    "Electronics", "Clothing", "Shoes", "Furniture", "Grocery (Non-Veg)", "Veg"
]


@slot_bp.route("/book-slot", methods=["GET", "POST"])
def book_slot():
    if 'user_id' not in session:
        return redirect(url_for("auth_bp.login"))

    user_id = ObjectId(session['user_id'])

    if request.method == "POST":
        date = request.form["date"]
        time = request.form["time"]
        branch = request.form["branch"]
        section = request.form["section"]

        # Check if this slot already exists and is booked
        existing = mongo.db.slots.find_one({
            "date": date,
            "time": time,
            "branch": branch,
            "section": section
        })
        print("Existing slot:", existing)

        if existing:
            if existing.get("booked_by") is not None:
                flash("This slot is already booked!", "danger")
            else:
                mongo.db.slots.update_one(
                    {"_id": existing["_id"]},
                    {"$set": {"booked_by": user_id}}
                )
                flash("Slot booked successfully!", "success")
        else:
            # Insert new slot
            mongo.db.slots.insert_one({
                "date": date,
                "time": time,
                "branch": branch,
                "section": section,
                "booked_by": user_id
            })
            flash("Slot created and booked!", "success")

        return redirect(url_for("slot_bp.book_slot"))

    # Fetch all slots for display
    all_slots = list(mongo.db.slots.find())
    return render_template("book_slot.html", slots=all_slots,
                           branches=BANGALORE_BRANCHES,
                           sections=STORE_SECTIONS)
