import os

# Define the absolute path of the project's root directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Key used by Flask for signing session cookies
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    
    # Database connection string
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
    
    # Disable event system modification tracking to save memory
    SQLALCHEMY_TRACK_MODIFICATIONS = False