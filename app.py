from flask import Flask
from config import Config
from models import db
import routes


def create_app():
    app = Flask(__name__)
    
    app.config.from_object(Config)
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
        routes.init_app(app)
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(port=8080, debug=True)