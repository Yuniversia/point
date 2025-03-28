from app import db
from sqlalchemy import func

class Category(db.Model):
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    coefficient = db.Column(db.Integer, nullable=False)
    
    # Отношения
    points = db.relationship('Point', backref='category', lazy='dynamic')

    def __init__(self, name: str, coefficient: int):
        self.name = name
        self.coefficient = coefficient


    # TO DO: Переделать на встроенные методы sql
    @staticmethod
    def coefficient_sum():
        sum = db.session.query(func.sum(Category.coefficient)).one()
        # sum = 0
        # for category in Category.query.all():
            # sum += category.coefficient
        
        return sum[0]
    
    def __repr__(self):
        return f'<Category {self.name}>'