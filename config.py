import os

class Config:
    def __init__(self):
        # Base directory of the project
        BASE_DIR = os.path.abspath(os.path.dirname(__file__))
        
        # Secret Key (with a local fallback)
        SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-fallback-key-change-in-prod'
        
        # Database URI
        SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                                  'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
        
        # Disable modification tracking
        SQLALCHEMY_TRACK_MODIFICATIONS = False