from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from .models import Enrollment
from .serializers import EnrollmentSerializer
from rest_framework.exceptions import PermissionDenied
import os 
from dotenv import load_dotenv

class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer

    def dispatch(self, request, *args, **kwargs):
        token = request.headers.get("Authorization")
        if token != os.getenv("SERVICES_TOKEN"):
            raise PermissionDenied("No autorizado")    # ← raise en lugar de return Response
        return super().dispatch(request, *args, **kwargs)
