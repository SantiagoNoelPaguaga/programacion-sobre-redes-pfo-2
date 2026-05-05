from flask import Flask
from .models import db
import os

def create_app():
    app = Flask(__name__, template_folder='../templates')
    app.secret_key = os.environ.get('SECRET_KEY', 'clave_por_defecto_pfo2')

    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, '../database.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()
    
    from .routes import main
    app.register_blueprint(main)

    return app