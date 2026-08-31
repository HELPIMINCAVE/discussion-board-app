import datetime
from flask_sqlalchemy import SQLAlchemy # Imports

db = SQLAlchemy()

# 1. User Model
class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

# 2. Post Model (Discussion Threads)
class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    
    # Timestamp for post creation (defaults to current UTC time)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    
    # Foreign Key linking to the author
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Relational link to all replies under this thread
    replies = db.relationship('Reply', backref='parent_post', cascade='all, delete-orphan', lazy=True)

# 3. Reply Model (Thread Responses)
class Reply(db.Model):
    __tablename__ = 'replies'