from app import db
from sqlalchemy import func

class Category(db.Model):
    __tablename__ = 'category'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    coefficient = db.Column(db.Integer, nullable=False)
    
    # Отношения
    points = db.relationship('Point', backref='category', lazy='dynamic', cascade="all, delete")
    total_point = db.relationship('Total_point', back_populates='category', cascade="all, delete-orphan")


    def __init__(self, name: str, coefficient: int):
        self.name = name
        self.coefficient = coefficient


    @staticmethod
    def coefficient_sum():
        sum = db.session.query(func.sum(Category.coefficient)).one()
        return sum[0]
    
    def __repr__(self):
        return f'<Category {self.name}>'