from flask import Blueprint, render_template, request, redirect, url_for, current_app, send_from_directory, send_file, flash
from flask_login import current_user
from sqlalchemy import desc

from threading import Thread
import redis
import json

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

# thread = Thread(target=my_func, args=('args'))

def max_point_cashing():
    for criterion in Category.query.all():
        max_point = Total_point.query.filter_by(category_id=criterion.id).order_by(desc(Total_point.total_point)).first()
        if not max_point:
            max_point = 0
        else:
            max_point = max_point.total_point
        r.set(f'{criterion.name}', max_point)

    return True

def cashing_top_by_group(group):
    classes = ClassGroup.query.filter_by(age_group=group).order_by(ClassGroup.name).all()
    criteria = Category.query.all()
    
    total_activs = {}
    coefficient_sum = Category.coefficient_sum()
    for school_class in classes: 
        activ_list = []

        for criterion in criteria:
            max_point = r.get(f'{criterion.name}') # Get data from redis to optimize code
            point = Total_point.query.filter_by(category_id=criterion.id, class_id=school_class.id).one_or_none()
            if point and max_point and int(max_point) != 0:
                activity = point.total_point / int(max_point)
            else:
                activity = 0
            
            activity = round(activity, 2)

            activity = activity * criterion.coefficient
            activ_list.append(activity)
            
            

        total_activs[f"{school_class.name}"] = round(sum(activ_list) / coefficient_sum, 2)

    mapping = {}
    sorted_activs = sorted(total_activs.items(), key=lambda item: item[1], reverse=True)
    for key, item in sorted_activs:
        mapping[key] = item

    for field, value in mapping.items():
        r.hset(f"{group}", field, value)
        r.rpush(f"{group}_classes", str(field))

from app.models.class_group import ClassGroup
from app.models.user import User
from app.models.point import Point
from app.models.total_points import Total_point
from app.models.category import Category

import random
import os

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():

    group = request.args.get('group', default=None, type=str)
    if group == None:
        return redirect(url_for('main.index') + "?group=young")
    
    try:
        r.flushdb()
        max_point_cashing()
        cashing_top_by_group(group)

        classes = ClassGroup.query.filter_by(age_group=group).order_by(ClassGroup.name).all()
    
        top = r.lrange(f"{group}_classes", 0, 2) # get three first elements how list [2.a, 2.b, 3.a]
        activity = r.hmget(group, top) # get results by first three index

        return render_template('index.html', classes = classes, group=group, top=top, activity = activity)
    except:
        return render_template('index.html', group=group)


@main_bp.route('/class')
def class_stat():
    id = request.args.get('id')
    school_class = ClassGroup.query.filter_by(id=id).one_or_none()

    if not school_class:
        flash('Klase nebija atrasta', 'error')
        return redirect(url_for('main.index'))

    all_classes = r.lrange(f"{school_class.age_group}_classes", 0, -1)

    activity = r.hmget(school_class.age_group, school_class.name)
    place = all_classes.index(school_class.name)

    criteria = {}
    adding = {}

    class Comment:
        def __init__(self, value, author, description):
            self.value = value
            self.author = author
            self.description = description

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

    classes_count = len(all_classes)

    first_place = r.lrange(f"{school_class.age_group}_classes", 0, 0)
    max_activity = r.hmget(school_class.age_group, first_place)

    return render_template('class.html', clase=school_class, activity=activity,
                            place=place, criteria=criteria, classes_count = classes_count,
                            adding = adding, max_activity = max_activity)

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
    
