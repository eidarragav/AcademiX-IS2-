from flask_sqlalchemy import SQLAlchemy # type: ignore
db = SQLAlchemy()

class Course(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable = False)
    description = db.Column(db.String(300), nullable= False)
    category = db.Column(db.String(100), nullable = False)
    level = db.Column(db.String(100), nullable = False)
    #user_id
    instructor_id = db.Column(db.Integer, nullable = False)

