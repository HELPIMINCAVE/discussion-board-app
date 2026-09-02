from flask import Flask
from config import Config
from models import *
import routes


def create_app():
    app = Flask(__name__)
    
    app.config.from_object(Config())
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
        
        app.register_blueprint(routes.bp)
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(port=6767, debug=True)