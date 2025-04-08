from flask import Blueprint, render_template, request, redirect, url_for, current_app, send_from_directory, send_file, flash
from flask_login import current_user
from sqlalchemy import desc
import redis

from app.models.cashing import cashing_top_by_group, max_point_cashing
from app.models.class_group import ClassGroup
from app.models.user import User
from app.models.point import Point
from app.models.total_points import Total_point
from app.models.category import Category

import random
import os
from threading import Thread

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

main_bp = Blueprint('main', __name__)

class Comment:
        def __init__(self, value, author, description):
            self.value = value
            self.author = author
            self.description = description

@main_bp.route('/')
def index():

    group = request.args.get('group', default=None, type=str)
    if group == None:
        return redirect(url_for('main.index') + "?group=young")
    
    classes = ClassGroup.query.filter_by(age_group=group).order_by(ClassGroup.name).all()

    try:
        r.flushdb()
        max_point_cashing()
        cashing_top_by_group(group)

        top = r.lrange(f"{group}_classes", 0, 2) # get three first elements how list [2.a, 2.b, 3.a]

        class School_classes:
            def __init__(self, name: str, place: int, activity: float):
                self.name = name
                self.place = place
                self.activity = activity
        top_clases = []
        for i in top:
            cl = r.hgetall(i)
            top_clases.append(School_classes(cl["name"], cl["place"], cl["activity"]))
        

        return render_template('index.html', classes = classes, group=group, top_clases = top_clases)
    except:
        return render_template('index.html', group=group, classes = classes)


@main_bp.route('/class')
def class_stat():
    id = request.args.get('id')
    school_class = ClassGroup.query.filter_by(id=id).one_or_none()

    if not school_class:
        flash('Klase nebija atrasta', 'error')
        return redirect(url_for('main.index'))

    all_classes = r.lrange(f"{school_class.age_group}_classes", 0, -1)
    classes_count = len(all_classes)
    classe = r.hgetall(school_class.name)

    criteria = {}
    adding = {}

    # Block to get all point adding by criterion
    for criterion in Total_point.query.filter_by(class_id=school_class.id).all():
        max_point = r.get(f'{criterion.category.name}')
        point = criterion.total_point

        criteria[criterion.category.name] = {point: int(max_point)}

        coms = []
        for points in Point.query.filter_by(class_id=school_class.id, category_id=criterion.category_id):
            table = Comment(value=points.value, 
                                        author=points.added_by,
                                        description=points.description)
            print("Category points: ", table.value)
            coms.append(table)
            
        adding[criterion.category.name] = coms

    return render_template('class.html', classe=classe,
                            criteria=criteria, classes_count = classes_count,
                            adding = adding)

@main_bp.route('/criterion')
def criteria():
    path = os.path.join('static/images/uploads/')
    print(path)

    try:
        return send_from_directory(path,'criterion.pdf')
    except FileNotFoundError as e:
        print(f"File not found error: {e}")
        flash('Fails nebija atrasts', 'error')
        return redirect(url_for('main.index'))
    
    except Exception as e:
        flash('Serverim ir problema', 'error')
        return redirect(url_for('main.index'))
    
@main_bp.route('/grafik')
def grafik():
    path = os.path.join('static/images/uploads/')
    print(path)

    try:
        return send_from_directory(path,'schedule.pdf')
    except FileNotFoundError as e:
        print(f"File not found error: {e}")
        flash('Fails nebija atrasts', 'error')
        return redirect(url_for('main.index'))
    
    except Exception as e:
        flash('Serverim ir problema', 'error')
        return redirect(url_for('main.index'))
    
