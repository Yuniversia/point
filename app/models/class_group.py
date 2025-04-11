from app import db
from app.models.point import Point

import random
from dataclasses import dataclass
from sqlalchemy import func, delete


class ClassGroup(db.Model):
    __tablename__ = 'class_groups'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    age_group = db.Column(db.String(10), nullable=False) 
    
    # Отношения
    points = db.relationship('Point', backref='class_group', lazy='dynamic', cascade="all, delete")
    # Отношение один ко многим из-за uselist
    total_point = db.relationship('Total_point', back_populates='class_group', cascade="all, delete-orphan")

    def __init__(self, name: str, age_group: str):
        self.name = name
        self.age_group = age_group

    @staticmethod
    def class_by_group(group):
        res = db.session.query(ClassGroup).filter_by(age_group=group).all()
        return res
    
    def __repr__(self):
        return f'<ClassGroup {self.name}>'
    
# Use in main.py and admin.py top classes
@dataclass
class School_classes:
    name: str
    id: int
    age_group: str
    place: int
    activity: float

# Use in main.py /class 
class Comment:
    def __init__(self, value, author, description):
        self.value = value
        self.author = author
        self.description = description
