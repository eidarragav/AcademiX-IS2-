from flask import jsonify, request, current_app
from models import Course, db

def register_routes(app):
    @app.route('/api/courses', methods = ['GET'])
    def get_courses():
        courses = Course.query.all()
        return jsonify([{'id': c.id,
                         'title' : c.title,
                         'description' : c.description,
                         'category' : c.category,
                         'level' : c.level,
                        } for c in courses])
    
    @app.route("/api/courses/<int:id>", methods = ['GET'])
    def get_course(id):
        course = Course.query.get_or_404(id)

        return jsonify({'id': course.id,
                         'title' : course.title,
                         'description' : course.description,
                         'category' : course.category,
                         'level' : course.level,
                        }), 200
        

    @app.route('/api/courses', methods = ['POST'])
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
    def delete_courses(id):
        course = Course.query.get_or_404(id)

        db.session.delete(course)
        db.session.commit()

        return jsonify({'STATUS' : 200})

