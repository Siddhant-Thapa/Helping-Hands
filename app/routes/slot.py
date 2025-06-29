from bson import ObjectId
from datetime import datetime
from datetime import datetime, timedelta
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


@slot_bp.route("/calendar-view")
def calendar_view():
    if 'user_id' not in session:
        return redirect(url_for('auth_bp.login'))

    user_id = str(session['user_id'])  # ✅ Pass as string

    today = datetime.today().date()
    next_seven_days = [today + timedelta(days=i) for i in range(7)]

    slots = list(mongo.db.slots.find({
        "date": {"$in": [d.strftime("%Y-%m-%d") for d in next_seven_days]}
    }))

    slot_map = {d.strftime("%Y-%m-%d"): [] for d in next_seven_days}
    for slot in slots:
        slot_map[slot["date"]].append(slot)

    return render_template("calendar_view.html", slot_map=slot_map, user_id=user_id, days=next_seven_days)


@slot_bp.route("/book-from-calendar", methods=["POST"])
def book_from_calendar():
    if 'user_id' not in session:
        return redirect(url_for("auth_bp.login"))

    user_id = ObjectId(session["user_id"])  # ✅ Important fix

    date = request.form["date"]
    time = request.form["time"]
    branch = request.form["branch"]
    section = request.form["section"]

    existing_booking = mongo.db.slots.find_one({
        "booked_by": user_id,
        "date": date,
        "branch": branch
    })

    if existing_booking:
        flash(
            f"You’ve already booked a slot in {branch} on {date}.", "warning")
        return redirect(url_for("slot_bp.calendar_view"))

    existing_slot = mongo.db.slots.find_one({
        "date": date,
        "time": time,
        "branch": branch,
        "section": section
    })

    if existing_slot:
        if existing_slot.get("booked_by"):
            flash("This slot is already booked!", "danger")
        else:
            mongo.db.slots.update_one(
                {"_id": existing_slot["_id"]},
                {"$set": {"booked_by": user_id}}  # ✅ This is now fixed
            )
            flash("Slot booked successfully!", "success")
    else:
        mongo.db.slots.insert_one({
            "date": date,
            "time": time,
            "branch": branch,
            "section": section,
            "booked_by": user_id
        })
        flash("Slot created and booked!", "success")

    return redirect(url_for("slot_bp.calendar_view"))


@slot_bp.route("/my-bookings")
def my_bookings():
    if 'user_id' not in session:
        return redirect(url_for('auth_bp.login'))

    user_id = ObjectId(session["user_id"])
    today = datetime.today().date()

    all_bookings = list(mongo.db.slots.find({
        "booked_by": user_id
    }).sort("date", 1))

    past = []
    upcoming = []

    for slot in all_bookings:
        try:
            # Accept both formats: "2025-07-02" and "2025/07/02"
            if "-" in slot["date"]:
                slot_date = datetime.strptime(slot["date"], "%Y-%m-%d").date()
            else:
                slot_date = datetime.strptime(slot["date"], "%Y/%m/%d").date()
        except Exception:
            continue

        # 🧠 Attach feedback info if it exists
        feedback = mongo.db.feedback.find_one({
            "user_id": user_id,
            "slot_id": slot["_id"]
        })

        if feedback:
            slot["feedback_given"] = True
            slot["rating"] = feedback["rating"]
            slot["comment"] = feedback.get("comment", "")
        else:
            slot["feedback_given"] = False

        # 🧠 Categorize as past or upcoming
        if slot_date < today:
            past.append(slot)
        else:
            upcoming.append(slot)

    return render_template("my_bookings.html", upcoming=upcoming, past=past)


@slot_bp.route("/cancel-booking/<slot_id>", methods=["POST"])
def cancel_booking(slot_id):
    if 'user_id' not in session:
        return redirect(url_for("auth_bp.login"))

    user_id = ObjectId(session["user_id"])

    slot = mongo.db.slots.find_one({"_id": ObjectId(slot_id)})

    if slot and slot.get("booked_by") == user_id:
        mongo.db.slots.update_one(
            {"_id": ObjectId(slot_id)},
            {"$unset": {"booked_by": ""}}  # Remove the booking
        )
        flash("Your booking has been cancelled.", "info")
    else:
        flash("You are not authorized to cancel this booking.", "danger")

    return redirect(url_for("slot_bp.my_bookings"))


@slot_bp.route("/create-slot", methods=["GET", "POST"])
def create_slot():
    if 'user_id' not in session:
        return redirect(url_for("auth_bp.login"))

    # 🚫 Temporary block everyone from accessing this route
    flash("🚫 This feature is restricted to admins.", "danger")
    return redirect(url_for("slot_bp.calendar_view"))
