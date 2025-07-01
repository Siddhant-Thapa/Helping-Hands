from app import create_app
from app.models import db, Branch, Section

app = create_app()
with app.app_context():
    # Branches
    for name in [
        "Indiranagar", "Whitefield", "Malleshwaram", "Koramangala", "HSR Layout"
    ]:
        if not Branch.query.filter_by(name=name).first():
            db.session.add(Branch(name=name))
    # Sections
    for name in [
        "Electronics", "Clothing", "Shoes", "Furniture", "Grocery (Non-Veg)", "Veg"
    ]:
        if not Section.query.filter_by(name=name).first():
            db.session.add(Section(name=name))
    db.session.commit()
    print("Branches and sections seeded!")
