"""
AcademiX - Pruebas de rendimiento: Evaluations Service
====================================================
"""

from locust import HttpUser, task, between  # type: ignore
import random

TEST_EMAIL    = "elkin.com"
TEST_PASSWORD = "1234"

SAMPLE_COURSE_IDS     = [3, 4, 5]
SAMPLE_EXAM_IDS       = [1,3,4]
SAMPLE_QUESTION_IDS   = ["1", "2"]
SAMPLE_SUBMISSION_IDS = ["1", "2"]


class EvaluationsUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        self.token = None
        self.created_exam_id = None
        self.created_question_id = None
        self.created_submission_id = None
        self._login()

    def _login(self):
        response = self.client.post(
            "/api/login",
            json={"email": TEST_EMAIL, "password": TEST_PASSWORD},
            name="[Auth] Login"
        )
        if response.status_code == 200:
            data = response.json()
            self.token = data.get("token") or data.get("access_token")

    def _headers(self):
        return {"Authorization": f"Bearer {self.token}"}


    @task(3)
    def listar_exams(self):
        with self.client.get(
            "/api/exams",
            headers=self._headers(),
            catch_response=True,
            name="[Exams] Listar"
        ) as r:
            r.success() if r.status_code == 200 else r.failure(f"{r.status_code}")

    @task(2)
    def obtener_exam(self):
        exam_id = self.created_exam_id or random.choice(SAMPLE_EXAM_IDS)

        with self.client.get(
            f"/api/exams/{exam_id}",
            headers=self._headers(),
            catch_response=True,
            name="[Exams] Obtener"
        ) as r:
            r.success() if r.status_code in (200, 404) else r.failure(f"{r.status_code}")

    @task(2)
    def crear_exam(self):
        payload = {
            "title": f"Exam {random.randint(1000,9999)}",
            "course_id": random.choice(SAMPLE_COURSE_IDS),
            "passing_score": random.randint(50, 90)
        }

        with self.client.post(
            "/api/exams",
            json=payload,
            headers=self._headers(),
            catch_response=True,
            name="[Exams] Crear"
        ) as r:
            if r.status_code in (200, 201):
                self.created_exam_id = r.json().get("id") or r.json().get("_id")
                r.success()
            else:
                r.failure(f"{r.status_code} - {r.text}")

    @task(2)
    def editar_exam(self):
        exam_id = random.choice(SAMPLE_EXAM_IDS)

        with self.client.put(
            f"/api/exams/{exam_id}",
            json={
                "title": f"Editado {random.randint(1,999)}",
                "course_id" : random.choice(SAMPLE_COURSE_IDS),
                "passing_score": random.randint(50, 90)
            },
            headers=self._headers(),
            catch_response=True,
            name="[Exams] Editar"
        ) as r:
            r.success() if r.status_code in (200, 201) else r.failure(f"{r.status_code}")

    @task(1)
    def eliminar_exam(self):
        payload = {
            "title": "Temporal",
            "course_id": random.choice(SAMPLE_COURSE_IDS),
            "passing_score": 60
        }

        with self.client.post(
            "/api/exams",
            json=payload,
            headers=self._headers(),
            catch_response=True,
            name="[Exams] Crear para eliminar"
        ) as r:
            if r.status_code in (200, 201):
                exam_id = r.json().get("id") or r.json().get("_id")
                r.success()

                if exam_id:
                    self.client.delete(
                        f"/api/exams/{exam_id}",
                        headers=self._headers(),
                        name="[Exams] Eliminar"
                    )
            else:
                r.failure(f"{r.status_code}")

    @task(3)
    def crear_question(self):
        

        payload = {
            "exam_id": random.choice(SAMPLE_EXAM_IDS),
            "text": "Pregunta de prueba",
            "option_a": "A",
            "option_b": "B",
            "option_c": "C",
            "option_d": "D",
            "correct_option": random.choice(["A", "B", "C", "D"])
        }

        with self.client.post(
            "/api/questions",
            json=payload,
            headers=self._headers(),
            catch_response=True,
            name="[Questions] Crear"
        ) as r:
            if r.status_code in (200, 201):
                self.created_question_id = r.json().get("id") or r.json().get("_id")
                r.success()
            else:
                r.failure(f"{r.status_code}")

    @task(2)
    def obtener_question(self):
        question_id = self.created_question_id or random.choice(SAMPLE_QUESTION_IDS)

        with self.client.get(
            f"/api/questions/{question_id}",
            headers=self._headers(),
            catch_response=True,
            name="[Questions] Obtener"
        ) as r:
            r.success() if r.status_code in (200, 404) else r.failure(f"{r.status_code}")

    @task(2)
    def editar_question(self):
        question_id = self.created_question_id or random.choice(SAMPLE_QUESTION_IDS)

        with self.client.put(
            f"/api/questions/{question_id}",
            json={
                "text": "Pregunta editada",
                "option_a": "A1",
                "option_b": "B1",
                "option_c": "C1",
                "option_d": "D1",
                "correct_option": "A"
            },
            headers=self._headers(),
            catch_response=True,
            name="[Questions] Editar"
        ) as r:
            r.success() if r.status_code in (200, 201) else r.failure(f"{r.status_code}")

    @task(1)
    def eliminar_question(self):

        payload = {
            "exam_id": random.choice(SAMPLE_QUESTION_IDS),
            "text": "Temp",
            "option_a": "A",
            "option_b": "B",
            "option_c": "C",
            "option_d": "D",
            "correct_option": "A"
        }

        with self.client.post(
            "/api/questions",
            json=payload,
            headers=self._headers(),
            catch_response=True,
            name="[Questions] Crear para eliminar"
        ) as r:
            if r.status_code in (200, 201):
                q_id = r.json().get("id") or r.json().get("_id")
                r.success()

                if q_id:
                    self.client.delete(
                        f"/api/questions/{q_id}",
                        headers=self._headers(),
                        name="[Questions] Eliminar"
                    )
            else:
                r.failure(f"{r.status_code}")


    @task(2)
    def listar_submissions(self):
        with self.client.get(
            "/api/submissions",
            headers=self._headers(),
            catch_response=True,
            name="[Submissions] Listar"
        ) as r:
            r.success() if r.status_code == 200 else r.failure(f"{r.status_code}")

    @task(2)
    def crear_submission(self):
        exam_id = self.created_exam_id or random.choice(SAMPLE_EXAM_IDS)

        payload = {
            "exam_id": exam_id,
            "score": random.randint(0, 100),
            "passed": random.choice([True, False])
        }

        with self.client.post(
            "/api/submissions",
            json=payload,
            headers=self._headers(),
            catch_response=True,
            name="[Submissions] Crear"
        ) as r:
            if r.status_code in (200, 201):
                self.created_submission_id = r.json().get("id") or r.json().get("_id")
                r.success()
            else:
                r.failure(f"{r.status_code}")

    @task(2)
    def obtener_submission(self):
        sub_id = self.created_submission_id or random.choice(SAMPLE_SUBMISSION_IDS)

        with self.client.get(
            f"/api/submissions/{sub_id}",
            headers=self._headers(),
            catch_response=True,
            name="[Submissions] Obtener"
        ) as r:
            r.success() if r.status_code in (200, 404) else r.failure(f"{r.status_code}")

    @task(2)
    def editar_submission(self):
        sub_id = self.created_submission_id or random.choice(SAMPLE_SUBMISSION_IDS)

        with self.client.put(
            f"/api/submissions/{sub_id}",
            json={
                "score": random.randint(0, 100),
                "passed": random.choice([True, False])
            },
            headers=self._headers(),
            catch_response=True,
            name="[Submissions] Editar"
        ) as r:
            r.success() if r.status_code in (200, 201) else r.failure(f"{r.status_code}")

    @task(1)
    def eliminar_submission(self):
        exam_id = self.created_exam_id or random.choice(SAMPLE_EXAM_IDS)

        payload = {
            "exam_id": exam_id,
            "score": 50,
            "passed": False
        }

        with self.client.post(
            "/api/submissions",
            json=payload,
            headers=self._headers(),
            catch_response=True,
            name="[Submissions] Crear para eliminar"
        ) as r:
            if r.status_code in (200, 201):
                sub_id = r.json().get("id") or r.json().get("_id")
                r.success()

                if sub_id:
                    self.client.delete(
                        f"/api/submissions/{sub_id}",
                        headers=self._headers(),
                        name="[Submissions] Eliminar"
                    )
            else:
                r.failure(f"{r.status_code}")



    def on_stop(self):
        if self.token:
            self.client.post(
                "/api/logout",
                headers=self._headers(),
                name="[Auth] Logout"
            )