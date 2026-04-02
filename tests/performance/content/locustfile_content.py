"""
AcademiX - Pruebas de rendimiento: Content Service
====================================================
"""

from locust import HttpUser, task, between  # type: ignore
import random

TEST_EMAIL    = "elkin.com"
TEST_PASSWORD = "1234"

SAMPLE_COURSE_IDS = [3, 4, 5]
SAMPLE_MODULES_IDS = ["69c9ba32bb38d80098dd7622", "69cee1f17df79db6d2183926", "69cee1f17df79db6d2183928"]
SAMPLE_LESSON_IDS = ["69c9c991e76312cd5e953524", "69c9c999e76312cd5e953527", "69c9c9e1e76312cd5e95352a"]  


class ContentUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        self.token = None
        self.created_module_id = None
        self.created_lesson_id = None
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

    # ---------------------------
    # 📦 MODULES
    # ---------------------------

    @task(4)
    def listar_modulos(self):
        lesson_id = random.choice(SAMPLE_LESSON_IDS)
        with self.client.get(
            f"/api/modules/{lesson_id}",
            headers=self._headers(),
            catch_response=True,
            name="[Modules] Listar módulos"
        ) as r:
            r.success() if r.status_code == 200 else r.failure(f"Error {r.status_code}")

    @task(2)
    def crear_modulo(self):
        payload = {
            "course_id": random.choice(SAMPLE_COURSE_IDS),
            "title": f"Modulo {random.randint(1000,9999)}",
            "description": "Modulo creado en prueba"
        }
        with self.client.post(
            "/api/modules",
            json=payload,
            headers=self._headers(),
            catch_response=True,
            name="[Modules] Crear módulo"
        ) as r:
            if r.status_code in (200, 201):
                data = r.json()
                self.created_module_id = data.get("id") or data.get("_id")
                r.success()
            else:
                r.failure(f"Error {r.status_code}")

    @task(2)
    def editar_modulo(self):

        with self.client.put(
            f"/api/modules/{random.choice(SAMPLE_MODULES_IDS)}",
            json={
                "course_id" : random.choice(SAMPLE_COURSE_IDS),
                "title": f"Editado {random.randint(1,999)}",
                "description": "Modulo actualizado"
            },
            headers=self._headers(),
            catch_response=True,
            name="[Modules] Editar módulo"
        ) as r:
            r.success() if r.status_code in (200, 201) else r.failure(f"Error {r.status_code}")

    @task(1)
    def eliminar_modulo(self):
 
        payload = {
            "course_id": random.choice(SAMPLE_COURSE_IDS),
            "title": f"Modulo eliminar {random.randint(1000,9999)}",
            "description": "Temporal"
        }

        with self.client.post(
            "/api/modules",
            json=payload,
            headers=self._headers(),
            catch_response=True,
            name="[Modules] Crear para eliminar"
        ) as r:
            if r.status_code in (200, 201):
                data = r.json()
                module_id = data.get("id") or data.get("_id")
                r.success()

                if module_id:
                    self.client.delete(
                        f"/api/modules/{module_id}",
                        headers=self._headers(),
                        name="[Modules] Eliminar módulo"
                    )
            else:
                r.failure(f"Error creando módulo: {r.status_code}")



    @task(3)
    def crear_lesson(self):
    
        payload = {
            "module_id": f"{random.choice(SAMPLE_MODULES_IDS)}",
            "title": f"Leccion {random.randint(1000,9999)}",
            "type": random.choice(["video", "text", "file"]),
            "content": {"data": "contenido prueba"}
        }

        with self.client.post(
            "/api/lessons",
            json=payload,
            headers=self._headers(),
            catch_response=True,
            name="[Lessons] Crear lección"
        ) as r:
            if r.status_code in (200, 201):
                data = r.json()
                self.created_lesson_id = data.get("id") or data.get("_id")
                r.success()
            else:
                r.failure(f"Error {r.status_code}")

    @task(2)
    def obtener_lesson(self):
        lesson_id = random.choice(SAMPLE_LESSON_IDS)

        with self.client.get(
            f"/api/lessons/{lesson_id}",
            headers=self._headers(),
            catch_response=True,
            name="[Lessons] Obtener lección"
        ) as r:
            r.success() if r.status_code in (200, 404) else r.failure(f"Error {r.status_code}")

    @task(2)
    def editar_lesson(self):
        lesson_id = random.choice(SAMPLE_LESSON_IDS)

        with self.client.put(
            f"/api/lessons/{lesson_id}",
            json={
                "title": f"Editada {random.randint(1,999)}",
                "type": "text",
                "content": {"data": "actualizado"}
            },
            headers=self._headers(),
            catch_response=True,
            name="[Lessons] Editar lección"
        ) as r:
            r.success() if r.status_code in (200, 201) else r.failure(f"Error {r.status_code}")

    @task(1)
    def eliminar_lesson(self):
        payload = {
            "module_id": random.choice(SAMPLE_MODULES_IDS),
            "title": f"Leccion {random.randint(1000,9999)}",
            "type": random.choice(["video", "text", "file"]),
            "content": {"data": "contenido prueba"}
        }

        with self.client.post(
            "/api/lessons",
            json=payload,
            headers=self._headers(),
            catch_response=True,
            name="[Lessons] Crear para eliminar"
        ) as r:
            if r.status_code in (200, 201):
                data = r.json()
                lesson_id = data.get("id") or data.get("_id")
                r.success()

                if lesson_id:
                    self.client.delete(
                        f"/api/lessons/{lesson_id}",
                        headers=self._headers(),
                        name="[Lesson] Eliminar lesson"
                    )
            else:
                r.failure(f"Error creando lesson: {r.status_code}")


    def on_stop(self):
        if self.token:
            self.client.post(
                "/api/logout",
                headers=self._headers(),
                name="[Auth] Logout"
            )