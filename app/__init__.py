import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config

db = SQLAlchemy()

def create_app(config_class=Config):
    app = Flask(__name__, static_folder="static", template_folder="templates")
    app.config.from_object(config_class)

    db.init_app(app)

    # Register blueprints
    from .routes import products, locations, movements
    app.register_blueprint(products.bp)
    app.register_blueprint(locations.bp)
    app.register_blueprint(movements.bp)

    # simple index route
    @app.route('/')
    def index():
        return app.send_static_file('index_redirect.html') if False else __import__('flask').render_template('index.html')

    return app
