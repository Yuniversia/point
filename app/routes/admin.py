from app import db
from app.models.user import User
from app.models.class_group import ClassGroup, School_classes
from app.models.category import Category
from app.models.point import Point
from app.models.total_points import Total_point
from app.models.cashing import cashing_top_by_group, max_point_cashing, r

import os
import json

from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user

admin_bp = Blueprint('admin', __name__)

@admin_bp.route("/", defaults={'group': 'young'})
@login_required
def main(group):

    group = request.args.get('group', default=None, type=str)
    if group == None:
        return redirect(url_for('admin.main') + "?group=young")

    user = User.query.filter_by(id=current_user.id).first()
    classes = ClassGroup.query.filter_by(age_group=group).order_by(ClassGroup.name).all()
    criteria = Category.query.all()
    
    try:
        top = r.lrange(f"{group}_classes", 0, -1) # get three first elements how list [2.a, 2.b, 3.a]

        filtered_classes = []
        for i in top:
            cl = r.hgetall(i)
            filtered_classes.append(School_classes(cl["name"], cl["id"], cl["age_group"], cl["place"], cl["activity"]))

        return render_template('admin/admin.html', group=group, user=user, classes = classes, criteria=criteria, filtered_classes=filtered_classes)
    
    except:
        return render_template('admin/admin.html', group=group, user=user, classes = classes, criteria=criteria)

@admin_bp.route("/points", methods=['POST'])
@login_required
def add_point():
    class_id = request.form.get("class_id")
    point_value = request.form.get("points")
    category_id = request.form.get("criterion_id")
    description = request.form.get("description")

    # Желательно группу получать как-то подругому
    group = db.session.get(ClassGroup, class_id)
    group = group.age_group

    point_class = Point(
        class_id=class_id,
        value=point_value,
        category_id = category_id,
        description= description,
        added_by= current_user.name
    )

    total_count = Total_point.query.filter_by(category_id=category_id, class_id=class_id).one_or_none()
    if not total_count:
        new_record = Total_point(category_id=category_id, class_id=class_id, point=point_value)

        db.session.add(new_record)
    else:
        total_count.total_point += int(point_value)

    try:
        db.session.add(point_class)
        db.session.commit()

        max_point_cashing(group)
        cashing_top_by_group(group)

        response = current_app.response_class(
            response=json.dumps({'success':True, "message": "Punkti bija veiksmīgi pievienoti"}),
            status=201,
            mimetype="application/json"
        )
        return response
    except:
        db.session.reset(point_class)

        response = current_app.response_class(
            response=json.dumps({'success':False, "message": "Notieka kļuda"}),
            status=502,
            mimetype="application/json"
        )
        return response

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@admin_bp.route("/files", methods=['POST'])
@login_required
def upload_file():
    file_type = request.form.get("file_type")

    if 'file' not in request.files:
        flash('No file part', 'error')
        return redirect(url_for('admin.main')), 301
    
    file = request.files['file']

    if file.filename == '':
        flash('No selected file', 'error')
        return redirect(url_for('admin.main')), 301
    
    split_name, file_extension = os.path.splitext(file.filename)

    if file and allowed_file(file.filename):
        filename = secure_filename(file_type)
        file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], f'{filename}{file_extension}'))

    flash('Fails bija veiksmigi pievienots', 'success')
    return redirect(url_for('admin.main')), 301

@admin_bp.route("/user", methods=['GET'])
@login_required
def user():
    user = User.query.filter_by(id=current_user.id).first()

    return render_template('admin/user.html', user=user), 302

@admin_bp.route("user/username", methods=['POST'])
@login_required
def change_username():
    username = request.form.get('username')
    user = User.query.filter_by(id=current_user.id).first()

    user.username = username
    db.session.commit()

    flash('Segvārds bija veiksmīgi mainīts', 'success')
    return redirect(url_for('admin.user')), 301

@admin_bp.route("user/password", methods=['POST'])
@login_required
def change_password():
    password = request.form.get('password')
    user = User.query.filter_by(id=current_user.id).first()

    user.password_hash = generate_password_hash(password)
    db.session.commit()

    flash('Parole bija vieksmīgi mainīta', 'success')
    return redirect(url_for('admin.user')), 200

@admin_bp.route("/classes", methods=['GET', 'POST'])
@login_required
def school_class():
    if not current_user.adding_classes:
        flash("Jūms nav tiesību", "error")
        return redirect(request.url)

    if request.method == 'POST':
        print("method post")
        name = request.form.get('name')
        group = request.form.get('group')

        cl = ClassGroup(
            name=name,
            age_group=group
        )

        db.session.add(cl)
        db.session.commit()

        flash('Klase veiksmīgi pievienota', 'success')
        return redirect(url_for('admin.school_class') + f"?group={group}")
    else:
        group = request.args.get('group', default=None, type=str)
        if group == None:
            return redirect(url_for('admin.school_class') + "?group=young"), 302

        user = User.query.filter_by(id=current_user.id).first()
        classes = ClassGroup.query.filter_by(age_group=group).order_by(ClassGroup.name).all()

        return render_template('admin/classes.html', group=group, user=user, classes = classes)


@admin_bp.route("/class/delete", methods=['POST'])
@login_required
def delete_class():
    if not current_user.adding_classes:
        flash("Jūms nav tiesību", "error")
        return redirect(request.url)
    
    id = request.form.get('id')

    school_class = db.session.get(ClassGroup, {"id": id})
    print(school_class)
    db.session.delete(school_class)
    db.session.commit()

    flash('Klase veiksmīgi dzēsta', 'success')
    return redirect(url_for('admin.school_class') + f"?group={school_class.age_group}"), 301

@admin_bp.route("/criteria")
@login_required
def criteria():
    if not current_user.adding_category:
        flash("Jūms nav tiesību", "error")
        return redirect(request.url)
    
    user = User.query.filter_by(id=current_user.id).first()
    criteria = Category.query.all()

    percentages = []
    sum = Category.coefficient_sum()

    for i in criteria:
        value = (i.coefficient / sum) * 100
        percentages.append(round(value, 2))

    
    return render_template('admin/criteria.html', user=user, criteria=criteria, percentages=percentages)

@admin_bp.route("/criteria", methods=['POST'])
@login_required
def add_criteria():
    if not current_user.adding_category:
        flash("Jūms nav tiesību", "error")
        return redirect(request.url)

    name = request.form.get('name')
    coefficient = request.form.get('coefficient')

    criteria = Category(
        name=name,
        coefficient = coefficient
    )

    db.session.add(criteria)
    db.session.commit()

    max_point_cashing("young")
    max_point_cashing("old")
    cashing_top_by_group("young")
    cashing_top_by_group("old")

    flash('Kriterijs bija veiksmīgi pievienots', 'success')
    return redirect(url_for('admin.criteria')), 302

@admin_bp.route("/criteria/change", methods=['POST'])
@login_required
def change_criteria():
    if not current_user.adding_category:
        flash("Jūms nav tiesību", "error")
        return redirect(request.url)

    id = request.form.get('id')
    name = request.form.get('name')
    coefficient = request.form.get('coefficient')

    criteria = Category.query.filter_by(id=id).first()

    criteria.name = name
    criteria.coefficient = coefficient

    db.session.commit()

    max_point_cashing("young")
    max_point_cashing("old")
    cashing_top_by_group("young")
    cashing_top_by_group("old")

    flash('Kriterijs bija veiksmīgi rediģets', 'success')
    return redirect(url_for('admin.criteria')), 302

@admin_bp.route("/criteria/delete", methods=['POST'])
@login_required
def delete_criteria():
    if not current_user.adding_category:
        flash("Jūms nav tiesību", "error")
        return redirect(request.url)

    id = request.form.get('id')

    criteria = Category.query.filter_by(id=id).first()

    db.session.delete(criteria)
    db.session.commit()

    max_point_cashing("young")
    max_point_cashing("old")
    cashing_top_by_group("young")
    cashing_top_by_group("old")

    flash('Kriterijs bija veiksmīgi dzēsts', 'success')
    return redirect(url_for('admin.criteria')), 302

@admin_bp.route('/administration')
@login_required
def administration():
    if not current_user.adding_users:
        flash("Jūms nav tiesību", "error")
        return redirect(request.url)
    
    user = User.query.filter_by(id=current_user.id).first()

    users = User.query.all()
    return render_template('admin/administration.html', user=user, users=users)

@admin_bp.route('/administration', methods=['POST'])
@login_required
def add_user():
    if not current_user.adding_users:
        flash("Jūms nav tiesību", "error")
        return redirect(request.url)

    username = request.form.get('username')
    name = request.form.get('name')
    password = request.form.get('password')
    adding_classes = request.form.get('adding_classes')
    adding_category = request.form.get('adding_category')
    adding_users = request.form.get('adding_users')

    u = User(
        username=username,
        name=name,
        password=password,
        adding_point= True,
        adding_classes= True if adding_classes == "on" else False,
        adding_category= True if adding_category == "on" else False,
        adding_users= True if adding_users == "on" else False,
        created_by=current_user.name
    )

    db.session.add(u)
    db.session.commit()

    flash('Lietotajs bija pievienots', 'success')
    return redirect(url_for('admin.administration')), 302

@admin_bp.route('/administration/delete', methods=['POST'])
@login_required
def delete_user():
    if current_user.adding_users:
        id = request.form.get('user_id')

        user = db.session.get(User, {"id": id})
        db.session.delete(user)
        db.session.commit()

        flash('Lietotajs bija veiksmīgi dzēsts', 'success')
        return redirect(url_for('admin.administration')), 302
    
    flash('Jus neesat administrators', 'error')
    return redirect(url_for('admin.administration')), 302