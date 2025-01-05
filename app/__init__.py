from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

load_dotenv()

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'df77ecd4d372091361511579f04aa697c6d73b5d5169f288')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    migrate.init_app(app, db)

    from .routes import main
    app.register_blueprint(main)
    
    # uncomment kode dibawah ini untuk menjalankan data seeder akun admin,
    # karena pada kasus ini untuk crud dapat dilakukan semua user login maka tidak perlu digunakan
    
    # with app.app_context():
    #     from .seeder import seed_data
    #     seed_data()
    

    return app