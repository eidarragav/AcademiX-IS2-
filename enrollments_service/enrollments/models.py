from django.db import models

class Enrollment(models.Model):
    user_id = models.IntegerField()
    course_id = models.IntegerField()
    status = models.CharField(max_length=100)