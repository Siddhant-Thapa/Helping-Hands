from app import create_app
from app.models import db, User
from datetime import datetime

# Create the Flask App Context
app = create_app()
with app.app_context():
    # Update all existing users to be approved (so they can still login)
    existing_users = User.query.all()

    for user in existing_users:
        updated = False

        # Set approval status if not set
        if user.approval_status is None or user.approval_status == '':
            user.approval_status = 'approved'
            user.is_approved = True
            updated = True

        # Set registered_at if not set
        if user.registered_at is None:
            user.registered_at = datetime.utcnow()
            updated = True

        if updated:
            print(
                f"Updated user: {user.name} ({user.email}) - Status: {user.approval_status}, Registered: {user.registered_at}")

    # Commit the changes
    db.session.commit()
    print(f"\nUpdated {len(existing_users)} existing users!")
    print("All existing users now have proper approval status and registration timestamps.")
    print("New registrations will require admin approval.")
