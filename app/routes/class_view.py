from flask import Blueprint, render_template, abort
from app.models.class_group import ClassGroup
from app.models.category import Category
from app.models.point import Point
from sqlalchemy import desc

class_bp = Blueprint('class', __name__)

@class_bp.route('/<int:class_id>')
def view(class_id):
    class_group = ClassGroup.query.get_or_404(class_id)
    
    # Получаем все баллы класса
    points = Point.query.filter_by(class_id=class_id).order_by(desc(Point.created_at)).all()
    
    # Получаем все категории
    categories = Category.query.all()
    categories_dict = {cat.id: cat for cat in categories}
    
    # Группируем баллы по категориям
    points_by_category = {}
    for point in points:
        if point.category_id in points_by_category:
            points_by_category[point.category_id]['value'] += point.value
            points_by_category[point.category_id]['entries'].append(point)
        else:
            points_by_category[point.category_id] = {
                'value': point.value,
                'name': categories_dict[point.category_id].name,
                'entries': [point]
            }
    
    # Суммарное количество баллов
    total_points = sum(item['value'] for item in points_by_category.values())
    
    return render_template('class/view.html', 
                           class_group=class_group,
                           points=points,
                           points_by_category=points_by_category,
                           total_points=total_points)