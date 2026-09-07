from flask import Flask
from flask_login import LoginManager
from config import Config
from models import db, User
import routes

login_manager = LoginManager()
login_manager.login_view = 'main.login'  # Redirects here if @login_required triggers
login_manager.login_message = "Please log in to access this page."


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


def create_app():
    app = Flask(__name__)
    
    app.config.from_object(Config)
    
    db.init_app(app)
    login_manager.init_app(app)
    
    with app.app_context():
        db.create_all()
        routes.init_app(app)
    
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(port=8080, debug=True)