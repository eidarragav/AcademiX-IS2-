from flask import jsonify, request, current_app
from models import Course, db
import os
from dotenv import load_dotenv # type: ignore
from functools import wraps


def require_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")
        if token!= os.getenv("SERVICES_TOKEN"):
            return jsonify({'error' : "no autorizado, token erroneo"}), 401
        return f(*args, **kwargs)
    return decorated

def register_routes(app):
    @app.route('/api/courses', methods = ['GET'])
    @require_token
    def get_courses():
        courses = Course.query.all()
        return jsonify([{'id': c.id,
                         'title' : c.title,
                         'description' : c.description,
                         'category' : c.category,
                         'level' : c.level,
                        } for c in courses])
    
    @app.route("/api/courses/<int:id>", methods = ['GET'])
    @require_token
    def get_course(id):
        course = Course.query.get_or_404(id)

        return jsonify({'id': course.id,
                         'title' : course.title,
                         'description' : course.description,
                         'category' : course.category,
                         'level' : course.level,
                        }), 200
        

    @app.route('/api/courses', methods = ['POST'])
    @require_token
    def post_courses():
        data = request.get_json()

        course = Course(
            title = data["title"],
            description = data["description"],
            category = data["category"],
            level = data["level"],
            instructor_id = data["instructor_id"],
        )

        db.session.add(course)
        db.session.commit()

        return jsonify({'id': course.id,
                         'title' : course.title,
                         'description' : course.description,
                         'category' : course.category,
                         'level' : course.level,
                        })
    
    @app.route('/api/courses/<int:id>', methods = ['PUT'])
    @require_token
    def update_courses(id):
        data = request.get_json()

        course = Course.query.get_or_404(id)
        course.title = data["title"]
        course.description = data["description"]
        course.category = data["category"]
        course.level = data["level"]

        db.session.commit()

        return jsonify({'id': course.id,
                         'title' : course.title,
                         'description' : course.description,
                         'category' : course.category,
                         'level' : course.level,
                        })
    

    @app.route('/api/courses/<int:id>', methods = ['DELETE'])
    @require_token
    def delete_courses(id):
        course = Course.query.get_or_404(id)

        db.session.delete(course)
        db.session.commit()

        return jsonify({'STATUS' : 200})

