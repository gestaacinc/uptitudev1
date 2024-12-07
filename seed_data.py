from app import app, db
from app.models import Staff

with app.app_context():
    # Add sample staff users with hashed passwords
    admin = Staff(name='Admin User', email='admin@example.com', password='admin123', role='admin', status='active')
    finance = Staff(name='Finance User', email='finance@example.com', password='finance123', role='finance', status='active')
    staff = Staff(name='Staff User', email='staff@example.com', password='staff123', role='staff', status='active')

    # Commit to the database
    db.session.add(admin)
    db.session.add(finance)
    db.session.add(staff)
    db.session.commit()

    print("Sample data with hashed passwords inserted successfully.")
