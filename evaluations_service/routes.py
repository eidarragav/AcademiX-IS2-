from flask import jsonify, request, current_app
from models import Exam, Submission, Question, db

def register_routes(app):
    @app.route('/api/exams', methods=['POST'])
    def create_exam():  
        data = request.json

        exam = Exam(
            course_id=data['course_id'],
            title=data['title'],
            passing_score=data['passing_score']
        )

        db.session.add(exam)
        db.session.commit()

        return jsonify({"message": "Exam creado", "id": exam.id})
    
    @app.route('/api/exams', methods=['GET'])
    def get_exams():
        exams = Exam.query.all()

        result = []
        for e in exams:
            result.append({
                "id": e.id,
                "title": e.title,
                "course_id": e.course_id,
                "passing_score": e.passing_score
            })

        return jsonify(result)
    
    @app.route('/api/exams/<int:id>', methods=['GET'])
    def get_exam(id):   
        exam = Exam.query.get_or_404(id)

        questions = []
        for q in exam.questions:
            questions.append({
                "id": q.id,
                "text": q.text,
                "option_a": q.option_a,
                "option_b": q.option_b,
                "option_c": q.option_c,
                "option_d": q.option_d
            })

        return jsonify({
            "id": exam.id,
            "title": exam.title,
            "course_id": exam.course_id,
            "passing_score": exam.passing_score,
            "questions": questions
        })
    
    @app.route('/api/exams/<int:id>', methods=['PUT'])
    def update_exam(id):
        exam = Exam.query.get_or_404(id)
        data = request.json

        exam.title = data.get('title', exam.title)
        exam.passing_score = data.get('passing_score', exam.passing_score)

        db.session.commit()

        return jsonify({"message": "Actualizado"})

    @app.route('/api/exams/<int:id>', methods=['DELETE'])
    def delete_exam(id):
        exam = Exam.query.get_or_404(id)

        db.session.delete(exam)
        db.session.commit()

        return jsonify({"message": "Eliminado"})