from rest_framework.test import APITestCase
from rest_framework import status
from .models import Enrollment
import os

TOKEN = "testtoken"
os.environ["SERVICES_TOKEN"] = TOKEN


class EnrollmentTests(APITestCase):

    def test_create_enrollment(self):
        data = {
            "user_id": 1,
            "course_id": 1,
            "status": "active"
        }

        response = self.client.post(
            "/api/enrollments/",
            data,
            format='json',
            HTTP_AUTHORIZATION=TOKEN
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Enrollment.objects.count(), 1)

    def test_get_enrollments(self):
        Enrollment.objects.create(user_id=1, course_id=1, status="active")

        response = self.client.get(
            "/api/enrollments/",
            HTTP_AUTHORIZATION=TOKEN
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_single_enrollment(self):
        enrollment = Enrollment.objects.create(
            user_id=1, course_id=1, status="active"
        )

        response = self.client.get(
            f"/api/enrollments/{enrollment.id}/",
            HTTP_AUTHORIZATION=TOKEN
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], enrollment.id)

    def test_update_enrollment(self):
        enrollment = Enrollment.objects.create(
            user_id=1, course_id=1, status="active"
        )

        data = {
            "user_id": 1,
            "course_id": 1,
            "status": "completed"
        }

        response = self.client.put(
            f"/api/enrollments/{enrollment.id}/",
            data,
            format='json',
            HTTP_AUTHORIZATION=TOKEN
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        enrollment.refresh_from_db()
        self.assertEqual(enrollment.status, "completed")

    def test_delete_enrollment(self):
        enrollment = Enrollment.objects.create(
            user_id=1, course_id=1, status="active"
        )

        response = self.client.delete(
            f"/api/enrollments/{enrollment.id}/",
            HTTP_AUTHORIZATION=TOKEN
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Enrollment.objects.count(), 0)