from config import Config

import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'main.index'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    db.init_app(app)
    login_manager.init_app(app)

    path = os.path.exists(app.config['UPLOAD_FOLDER'])
    if not path:
        path = os.path.join(app.config['UPLOAD_FOLDER'])
        os.makedirs(path)

    with app.app_context():
        from app.models import user
        from app.models import category
        from app.models import class_group
        from app.models import point
        from app.models import total_points

        db.create_all()

        # Creating admin
        from app.models.user import User

        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin',
                password='pass',
                name="Sergejs Deikuns",
                adding_point= True,
                adding_category= True,
                adding_classes= True,
                adding_users= True,
                created_by= 'System'
            )
            db.session.add(admin)
            db.session.commit()

        # Cashing data in redis after reboot
        from app.models.cashing import cashing_top_by_group, max_point_cashing

        max_point_cashing()
        cashing_top_by_group("young")
        cashing_top_by_group("old")
    
    from app.routes.main import main_bp
    from app.routes.auth import auth_bp
    from app.routes.admin import admin_bp
    from app.routes.class_view import class_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(class_bp, url_prefix='/class')
    
    return app