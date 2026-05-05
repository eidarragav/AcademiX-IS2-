from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
from config import Config
from models import db
import routes

def create_app(test_config=None):
    app = Flask(__name__)

    if test_config:
        app.config.update(test_config)
    else:
        app.config.from_object(Config)

    db.init_app(app)
    Migrate(app, db)
    CORS(app)

    routes.register_routes(app)

    return app



if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)