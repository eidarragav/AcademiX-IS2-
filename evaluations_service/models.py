from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


class Exam(db.Model):
    __tablename__ = 'exams'
    id = db.Column(db.Integer, primary_key = True)
    course_id = db.Column(db.Integer, nullable = False)
    title = db.Column(db.String(30), nullable= False)
    passing_score = db.Column(db.Integer, nullable = False)

class Question(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key = True)
    exam_id = db.Column(db.Integer, nullable = False)
    text = db.Column(db.String(200), nullable= False)
    option_a = db.Column(db.String(200), nullable = False)
    option_b = db.Column(db.String(200), nullable = False)
    option_c = db.Column(db.String(200), nullable = False)
    option_d = db.Column(db.String(200), nullable = False)
    correct_option = db.Column(db.String(2), nullable = False)
