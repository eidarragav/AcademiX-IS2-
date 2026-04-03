"""
AcademiX - Pruebas de rendimiento: Courses Service
====================================================
Todas las peticiones pasan por el API Gateway (puerto 8000).
 
Cómo correr:
  locust -f locustfile_courses.py --host=http://localhost:8000
 
Luego abrir http://localhost:8089 y configura desde la interfaz:
 
  Prueba de capacidad  → Users: 10  | Spawn rate: 1  | Tiempo: ~3 min
  Prueba de carga      → Users: 30  | Spawn rate: 3  | Tiempo: ~2 min
  Prueba de estrés     → Users: 100 | Spawn rate: 10 | Tiempo: ~2 min
 
"""
 
from locust import HttpUser, task, between # type: ignore
import random
 
TEST_EMAIL    = "elkin.com"
TEST_PASSWORD = "1234"
 
SAMPLE_COURSE_IDS = [3,4,5]
 
 
class CoursesUser(HttpUser):
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
    def listar_cursos(self):
        with self.client.get(
            "/api/courses",
            headers=self._headers(),
            catch_response=True,
            name="[Courses] Listar cursos"
        ) as r:
            r.success() if r.status_code == 200 else r.failure(f"Error {r.status_code}")
 
    @task(4)
    def obtener_curso(self):
        course_id = random.choice(SAMPLE_COURSE_IDS)
        with self.client.get(
            f"/api/courses/{course_id}",
            headers=self._headers(),
            catch_response=True,
            name="[Courses] Obtener curso"
        ) as r:
            r.success() if r.status_code in (200, 404) else r.failure(f"Error {r.status_code}")
 
    @task(2)
    def crear_curso(self):
        payload = {
            "title":         f"Curso prueba {random.randint(1000, 9999)}",
            "description":   "Curso generado por prueba de rendimiento.",
            "category":      random.choice(["Programación", "Diseño", "Data Science"]),
            "level":         random.choice(["beginner", "intermediate", "advanced"]),
            "instructor_id": 1,
        }
        with self.client.post(
            "/api/courses",
            json=payload,
            headers=self._headers(),
            catch_response=True,
            name="[Courses] Crear curso"
        ) as r:
            if r.status_code in (200, 201):
                data = r.json()
                self.created_course_id = data.get("id") or data.get("data", {}).get("id")
                r.success()
            else:
                r.failure(f"Error {r.status_code} — {r.text[:80]}")
 
    @task(2)
    def editar_curso(self):
        # Usa un ID conocido de la BD, no depende de que crear haya corrido antes
        course_id = random.choice(SAMPLE_COURSE_IDS)
        with self.client.put(
            f"/api/courses/{course_id}",
            json={
                "title":       f"Editado {random.randint(1, 999)}",
                "description": "Actualizado por prueba de rendimiento.",
                "category":    "Programación",
                "level":       "intermediate",
            },
            headers=self._headers(),
            catch_response=True,
            name="[Courses] Editar curso"
        ) as r:
            r.success() if r.status_code in (200, 201) else r.failure(f"Error {r.status_code}")
 
    @task(1)
    def eliminar_curso(self):
        # Crea un curso temporal y lo elimina en la misma tarea
        payload = {
            "title":         f"Curso a eliminar {random.randint(1000, 9999)}",
            "description":   "Curso temporal para prueba de eliminación.",
            "category":      "Programación",
            "level":         "beginner",
            "instructor_id": 1,
        }
        with self.client.post(
            "/api/courses",
            json=payload,
            headers=self._headers(),
            catch_response=True,
            name="[Courses] Crear para eliminar"
        ) as r:
            if r.status_code in (200, 201):
                data = r.json()
                course_id = data.get("id") or data.get("data", {}).get("id")
                r.success()
                if course_id:
                    self.client.delete(
                        f"/api/courses/{course_id}",
                        headers=self._headers(),
                        name="[Courses] Eliminar curso"
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