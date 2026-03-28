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
        }), 200
    
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
    
#Questions
    @app.route('/api/questions', methods=['POST'])
    def create_question():
        data = request.json

        question = Question(
            exam_id=data['exam_id'],
            text=data['text'],
            option_a=data['option_a'],
            option_b=data['option_b'],
            option_c=data['option_c'],
            option_d=data['option_d'],
            correct_option=data['correct_option']
        )

        db.session.add(question)
        db.session.commit()

        return jsonify({
                        "id" : question.id,
                        "exam_id" : question.exam_id,
                        "text" : question.text,
                        "option_a" : question.option_a,
                        "option_b" : question.option_b,
                        "option_c" : question.option_c,
                        "option_d" : question.option_d,
                        "correct_option" : question.correct_option,
                        })
    
    @app.route('/api/questions', methods=['GET'])
    def get_questions():
        questions = Question.query.all()

        result = []
        for q in questions:
            result.append({
                "id": q.id,
                "text": q.text,
                "correct_option": q.correct_option
            })

        return jsonify(result)
    
    @app.route('/api/questions/<int:id>', methods=['PUT'])
    def update_question(id):
        q = Question.query.get_or_404(id)
        data = request.json

        q.exam_id=data['exam_id'],
        q.text=data['text'],
        q.option_a=data['option_a'],
        q.option_b=data['option_b'],
        q.option_c=data['option_c'],
        q.option_d=data['option_d'],
        q.correct_option=data['correct_option']

        db.session.commit()

        return jsonify({
                        "id" : q.id,
                        "exam_id" : q.exam_id,
                        "text" : q.text,
                        "option_a" : q.option_a,
                        "option_b" : q.option_b,
                        "option_c" : q.option_c,
                        "option_d" : q.option_d,
                        "correct_option" : q.correct_option,
                        })
    
    @app.route('/api/questions/<int:id>', methods=['DELETE'])
    def delete_question(id):
        q = Question.query.get_or_404(id)

        db.session.delete(q)
        db.session.commit()

        return jsonify({"message": "Eliminada"})
    
    #Submissions
    @app.route('/api/submissions', methods=['POST'])
    def create_submission():
        data = request.json

        submission = Submission(
            exam_id=data['exam_id'],
            user_id=data['user_id'],
            score=data['score'],
            passed=data['passed']
        )

        db.session.add(submission)
        db.session.commit()

        return jsonify({"exam_id" : submission.exam_id, "user_id" : submission.user_id, "score" : submission.score, "passed" : submission.passed})
    
    @app.route('/api/submissions', methods=['GET'])
    def get_submissions():
        subs = Submission.query.all()

        return jsonify([
            {
                "id": s.id,
                "exam_id": s.exam_id,
                "user_id": s.user_id,
                "score": s.score,
                "passed": s.passed
            } for s in subs
        ])
    
    @app.route('/api/submissions/<int:id>', methods=['PUT'])
    def update_submission(id):
        s = Submission.query.get_or_404(id)
        data = request.json

        s.score = data.get('score', s.score)
        s.passed = data.get('passed', s.passed)

        db.session.commit()

        return jsonify({"exam_id" : s.exam_id, "user_id" : s.user_id, "score" : s.score, "passed" : s.passed})

    
    @app.route('/api/submissions/<int:id>', methods=['DELETE'])
    def delete_submission(id):
        s = Submission.query.get_or_404(id)

        db.session.delete(s)
        db.session.commit()

        return jsonify({"message": "Eliminada"})