# AcademiX — Plataforma Educativa

AcademiX es una plataforma educativa tipo Moodle construida sobre una 
arquitectura de microservicios. El sistema está compuesto por cinco 
microservicios independientes que se comunican exclusivamente a través 
de un API Gateway central.

## Microservicios

| Servicio | Framework | Base de datos | Puerto |
|---|---|---|---|
| API Gateway + Usuarios | Laravel 11 | MySQL | 8000 |
| Courses | Flask | MySQL | 5000 |
| Content | Express | MongoDB | 3000 |
| Enrollments | Django | PostgreSQL | 8080 |
| Evaluations | Flask | MySQL | 5001 |

## Documentación completa

La documentación técnica del proyecto incluyendo arquitectura, 
endpoints, guía de despliegue y resultados de pruebas de rendimiento 
está disponible aquí:

📄 [Ver documentación completa](docs/DocumentacionIS.pdf)

## Despliegue rápido

Consulta la sección de despliegue en la documentación para un mejor paso a paso o sigue este resumen:

1. Clona el repositorio
2. Configura las bases de datos (MySQL, PostgreSQL, MongoDB)
3. Copia y configura el `.env` de cada servicio
4. Levanta cada servicio en su puerto correspondiente

## Pruebas de rendimiento

Las pruebas se ejecutan con Locust:

\`\`\`bash
pip install locust
locust -f tests/performance/courses/locustfile_courses.py \
  --host=http://localhost:8000
\`\`\`

Abre http://localhost:8089 para la interfaz web.