# Note: karena pada kasus ini untuk crud dapat dilakukan semua user login maka tidak perlu digunakan

from . import db
from app.models import User
from werkzeug.security import generate_password_hash

def seed_data():
    if not User.query.first():
        password = 'admin12345'
        hashed_password = generate_password_hash(password)
        user1 = User(username='admin', role='admin', email='admin@admin.com', hashed_password=hashed_password )

        db.session.add(user1)
        db.session.commit()