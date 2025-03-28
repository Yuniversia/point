from app import db

class Total_point(db.Model):
    __tablename__ = 'total_points'
    
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('class_groups.id'), nullable=False)
    total_point = db.Column(db.Integer)

    def __init__(self, category_id: int, class_id: int, point: int = 0):
        self.category_id = category_id
        self.class_id = class_id
        self.total_point = point
