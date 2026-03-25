from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


class Exam(db.Model):
    __tablename__ = 'exams'
    id = db.Column(db.Integer, primary_key = True)
    course_id = db.Column(db.Integer, nullable = False)
    title = db.Column(db.String(30), nullable= False)
    passing_score = db.Column(db.Integer, nullable = False)

