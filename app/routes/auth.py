from app.models.user import User
from config import Login_conf

from datetime import timedelta

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user
from sqlalchemy import desc

auth_bp = Blueprint('login', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and User.check_password(user.password_hash, password):
            login_user(user, duration=timedelta(seconds=Login_conf.login_time))
            return redirect(url_for('admin.main'))
        else:
            flash('Nepareizs lietotajs vai parole', 'error')
            return redirect(url_for('main.index'))
    
    return redirect(url_for('main.index'))

@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))