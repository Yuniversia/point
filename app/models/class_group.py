from app import db
import random
from sqlalchemy import func, delete
from app.models.point import Point

class ClassGroup(db.Model):
    __tablename__ = 'class_groups'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    age_group = db.Column(db.String(10), nullable=False) 
    
    # Отношения
    points = db.relationship('Point', backref='class_group', lazy='dynamic', cascade="all, delete")
    total_point = db.relationship('Total_point', backref='class_group', lazy='dynamic', cascade="all, delete")

    def __init__(self, name: str, age_group: str):
        self.name = name
        self.age_group = age_group

    @staticmethod
    def class_by_group(group):
        res = db.session.query(ClassGroup).filter_by(age_group=group).all()
        return res
    
    @staticmethod
    def total_points_by_category(class_id: int, category_id: int):
        # return sum(point.value for point in self.points)
        # return random.randint(0, 150)
        sum = 0
        for point in Point.query.filter(class_id=class_id, category_id=category_id).all():
            sum += point.value
        
        return sum
    
    def points_by_category(self):
        # Возвращает словарь {категория_id: сумма_баллов}
        result = {}
        for point in self.points:
            if point.category_id in result:
                result[point.category_id] += point.value
            else:
                result[point.category_id] = point.value
        return result
    
    def __repr__(self):
        return f'<ClassGroup {self.name}>'
    
# Use in main.py and admin.py top classes 
class School_classes:
            def __init__(self, name: str, id: int, place: int, activity: float):
                self.name = name
                self.id = id
                self.place = place
                self.activity = activity

# Use in main.py /class 
class Comment:
        def __init__(self, value, author, description):
            self.value = value
            self.author = author
            self.description = description