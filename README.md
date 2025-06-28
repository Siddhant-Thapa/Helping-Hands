# Helping Hands – Staff Slot Booking System

Helping Hands is a Python Flask web application designed to allocate non-technical staff (like CEOs, managers, engineers) to assist customers during high-traffic sale seasons in large supermarkets like Big Bazaar or Walmart.

This system allows users to register, manage profiles, and book assistance slots at specific branches and departments.

---

## 🚀 Features

- 🔐 User Registration & Login (MongoDB-based)
- 👤 Profile Management with Profile Picture Upload
- 📍 Book Assistance Slots by:
  - Date and Time
  - Branch (5 Bangalore locations)
  - Section (Electronics, Clothing, Shoes, etc.)
- 🔒 Slots visually marked as Booked 🔐 or Available ✅
- 📦 Booking data stored in MongoDB
- 💬 Flash messages for feedback on actions

---

## 🗂️ Technologies Used

- **Python 3.11+**
- **Flask** (web framework)
- **MongoDB** (via Flask-PyMongo)
- **HTML5 + CSS3** (with basic custom styling)
- **MongoDB Compass** for DB inspection

---

## 📸 Screenshots

> _(Add screenshots here after you finish the UI polish — optional)_

---

## 🛠️ Setup Instructions

```bash
# Clone the repo
git clone https://github.com/yourusername/helping-hands.git
cd helping-hands

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows

# Install requirements
pip install -r requirements.txt

# Run the app
python run.py
