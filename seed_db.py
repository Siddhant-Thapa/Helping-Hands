from app import create_app
from app.models import db, Branch, Section

# Create the Flask App Context
app = create_app()
with app.app_context():
    # Seed Branches
    for name in [
        "Indiranagar", "Whitefield", "Malleshwaram", "Koramangala", "HSR Layout"
    ]:
        if not Branch.query.filter_by(name=name).first():
            db.session.add(Branch(name=name))
    # Seed Sections
    for name in [
        "Electronics", "Clothing", "Shoes", "Furniture", "Grocery (Non-Veg)", "Veg"
    ]:
        if not Section.query.filter_by(name=name).first():
            db.session.add(Section(name=name))

    # Commit the Session & Confirmation Message
    db.session.commit()
    print("Branches and sections seeded!")
