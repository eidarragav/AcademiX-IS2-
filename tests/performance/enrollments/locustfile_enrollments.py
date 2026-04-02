"""
AcademiX - Pruebas de rendimiento: Enrollments Service
=======================================================
Todas las peticiones pasan por el API Gateway (puerto 8000).

Cómo correr:
  locust -f locustfile_enrollments.py --host=http://localhost:8000

Luego abrir http://localhost:8089 y configura desde la interfaz:

  Prueba de capacidad  → Users: 10  | Spawn rate: 1  | Tiempo: ~3 min
  Prueba de carga      → Users: 30  | Spawn rate: 3  | Tiempo: ~2 min
  Prueba de estrés     → Users: 100 | Spawn rate: 10 | Tiempo: ~2 min

"""

from locust import HttpUser, task, between
import random

TEST_EMAIL    = "elkin.com"
TEST_PASSWORD = "1234"

# IDs de cursos que ya existen en tu BD
SAMPLE_COURSE_IDS = [3, 4, 5]

# IDs de inscripciones que ya existen en tu BD
SAMPLE_ENROLLMENT_IDS = [13, 14, 15]


class EnrollmentsUser(HttpUser):
    wait_time = between(1, 3)
 
    def on_start(self):
        self.token = None
        self.created_course_id = None
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

    @task(5)
    def listar_inscripciones(self):
        with self.client.get(
            "/api/enrollments",
            headers=self._headers(),
            catch_response=True,
            name="[Enrollments] Listar inscripciones"
        ) as r:
            r.success() if r.status_code == 200 else r.failure(f"Error {r.status_code}")

    @task(4)
    def obtener_inscripcion(self):
        enrollment_id = random.choice(SAMPLE_ENROLLMENT_IDS)
        with self.client.get(
            f"/api/enrollments/{enrollment_id}",
            headers=self._headers(),
            catch_response=True,
            name="[Enrollments] Obtener inscripcion"
        ) as r:
            r.success() if r.status_code in (200, 404) else r.failure(f"Error {r.status_code}")

    @task(2)
    def crear_inscripcion(self):
        payload = {
            "course_id": random.choice(SAMPLE_COURSE_IDS),
            "status":    "active",
        }
        with self.client.post(
            "/api/enrollments",
            json=payload,
            headers=self._headers(),
            catch_response=True,
            name="[Enrollments] Crear inscripcion"
        ) as r:
            if r.status_code in (200, 201):
                r.success()
            else:
                r.failure(f"Error {r.status_code} — {r.text[:80]}")

    @task(2)
    def editar_inscripcion(self):
        enrollment_id = random.choice(SAMPLE_ENROLLMENT_IDS)
        with self.client.put(
            f"/api/enrollments/{enrollment_id}",
            json={"status": random.choice(["active", "completed", "cancelled"])},
            headers=self._headers(),
            catch_response=True,
            name="[Enrollments] Editar inscripcion"
        ) as r:
            r.success() if r.status_code in (200, 201) else r.failure(f"Error {r.status_code}")

    @task(1)
    def eliminar_inscripcion(self):
        # Crea una inscripcion temporal y la elimina en la misma tarea
        payload = {
            "course_id": random.choice(SAMPLE_COURSE_IDS),
            "status":    "active",
        }
        with self.client.post(
            "/api/enrollments",
            json=payload,
            headers=self._headers(),
            catch_response=True,
            name="[Enrollments] Crear para eliminar"
        ) as r:
            if r.status_code in (200, 201):
                data = r.json()
                enrollment_id = data.get("id") or data.get("data", {}).get("id")
                r.success()
                if enrollment_id:
                    self.client.delete(
                        f"/api/enrollments/{enrollment_id}",
                        headers=self._headers(),
                        name="[Enrollments] Eliminar inscripcion"
                    )
            else:
                r.failure(f"Error al crear para eliminar: {r.status_code}")

    def on_stop(self):
        if self.token:
            self.client.post(
                "/api/logout",
                headers=self._headers(),
                name="[Auth] Logout"
            )