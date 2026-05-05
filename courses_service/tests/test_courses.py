import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from app import create_app
from models import db, Course

@pytest.fixture
def client():
    app = create_app({
    'TESTING': True,
    'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'
    })


    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()

TOKEN = "testtoken"
os.environ["SERVICES_TOKEN"] = TOKEN

HEADERS = {
    "Authorization": TOKEN
}

def test_create_course(client):
    response = client.post('/api/courses',
        json={
            "title": "Curso Test",
            "description": "Descripcion",
            "category": "Backend",
            "level": "Basico",
            "instructor_id": 1
        },
        headers=HEADERS
    )

    assert response.status_code == 200
    data = response.get_json()
    assert data["title"] == "Curso Test"

def test_get_courses(client):
    course = Course(
        title="Curso 1",
        description="Desc",
        category="Backend",
        level="Basico",
        instructor_id=1
    )
    db.session.add(course)
    db.session.commit()

    response = client.get('/api/courses', headers=HEADERS)

    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1


def test_get_single_course(client):
    course = Course(
        title="Curso 1",
        description="Desc",
        category="Backend",
        level="Basico",
        instructor_id=1
    )
    db.session.add(course)
    db.session.commit()

    response = client.get(f'/api/courses/{course.id}', headers=HEADERS)

    assert response.status_code == 200
    data = response.get_json()
    assert data["id"] == course.id

def test_update_course(client):
    course = Course(
        title="Viejo",
        description="Desc",
        category="Backend",
        level="Basico",
        instructor_id=1
    )
    db.session.add(course)
    db.session.commit()

    response = client.put(f'/api/courses/{course.id}',
        json={
            "title": "Nuevo",
            "description": "Nueva",
            "category": "Frontend",
            "level": "Avanzado"
        },
        headers=HEADERS
    )

    assert response.status_code == 200
    data = response.get_json()
    assert data["title"] == "Nuevo"

def test_delete_course(client):
    course = Course(
        title="Curso",
        description="Desc",
        category="Backend",
        level="Basico",
        instructor_id=1
    )
    db.session.add(course)
    db.session.commit()

    response = client.delete(f'/api/courses/{course.id}', headers=HEADERS)

    assert response.status_code == 200

    deleted = db.session.get(Course, course.id)
    assert deleted is None

