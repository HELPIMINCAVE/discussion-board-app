# seed.py
from app import create_app
from models import db, User

username = input("Enter username: ")
app = create_app()

with app.app_context():
    # Prevent duplicate user errors on multiple runs
    existing_user = User.query.filter_by(username=username).first()
    
    if not existing_user:
        test_user = User(username=username, email=f'{username}@example.com')
        db.session.add(test_user)
        db.session.commit()
        print(f"Created test user '{test_user.username}' with ID: {test_user.id}")
    else:
        print(f"User '{existing_user.username}' already exists with ID: {existing_user.id}")