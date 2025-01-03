from flask import Flask
from flask_wtf.csrf import CSRFProtect
from app.controllers import main_blueprint

csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'my_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

    csrf.init_app(app)

    app.register_blueprint(main_blueprint)

    return app