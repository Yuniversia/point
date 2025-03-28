from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    name = db.Column(db.String(120))
    password_hash = db.Column(db.String(128))

    adding_point = db.Column(db.Boolean, default=False)
    adding_classes = db.Column(db.Boolean, default=False)
    adding_category = db.Column(db.Boolean, default=False)
    adding_users = db.Column(db.Boolean, default=False)

    created_by = db.Column(db.String(120))
    
    def __init__(self, username: str, name: str, password: str, adding_point: bool,
                  adding_classes: bool, adding_category: bool, adding_users: bool, created_by='System'):
        self.username = username
        self.name = name
        self.password_hash = generate_password_hash(password)
        self.adding_point = adding_point
        self.adding_classes = adding_classes
        self.adding_category = adding_category
        self.adding_users = adding_users
        self.created_by = created_by
    
    @staticmethod
    def check_password(password_hash, password):
        return check_password_hash(password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))