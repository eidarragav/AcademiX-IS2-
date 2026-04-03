from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from .models import Enrollment
from .serializers import EnrollmentSerializer
import os 
from dotenv import load_dotenv

class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer

    def dispatch(self, request, *args, **kwargs):
        token = request.headers.get("Authorization")

        if token != os.getenv("SERVICES_TOKEN"):
            return Response(
                {"error": "No autorizado"},
                status=status.HTTP_403_FORBIDDEN
            )

        return super().dispatch(request, *args, **kwargs)
