from app import db

from sqlalchemy import func, delete


class Events(db.Model):
    __tablename__ = 'events'
    
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String(400), nullable=False) 
    date = db.Column(db.Date)


    def __init__(self, author: str, name: str, description: str, date: str):
        self.author = author
        self.name = name
        self.description = description
        self.date = date

    def delete_events(date):
        e = Events.query.filter(Events.date < date).delete()

        db.session.commit()
        
    
    def __repr__(self):
        return f'<ClassGroup {self.name}>'
