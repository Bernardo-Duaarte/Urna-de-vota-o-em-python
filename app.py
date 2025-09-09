from flask import Flask, render_template
from flask_cors import CORS
from config import Config
from models import db
from routes import routes

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)

    db.init_app(app)
    app.register_blueprint(routes)

    @app.route('/')
    def index():
        return render_template('index.html')

    return app
