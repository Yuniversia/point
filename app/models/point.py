from app import db
from sqlalchemy import func
from datetime import datetime

class Point(db.Model):
    __tablename__ = 'points'
    
    id = db.Column(db.Integer, primary_key=True)
    # class_id внешний ключ
    class_id = db.Column(db.Integer, db.ForeignKey('class_groups.id'), nullable=False)
    value = db.Column(db.Integer, nullable=False)
    # category_id внешний ключ
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, server_default=func.now())   
    # added_by внешние ключ
    added_by = db.Column(db.String(120))

    def __init__(self, class_id: int, value: int, category_id: int, description: str, added_by: int):
        self.class_id = class_id
        self.value = value
        self.category_id = category_id
        self.description = description
        self.added_by = added_by
    
    def __repr__(self):
        return f'<Point {self.id}: {self.value} для класса {self.class_id}>'