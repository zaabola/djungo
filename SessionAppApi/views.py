from django.shortcuts import render
from rest_framework import viewsets
from SessionApp.models import Session
from .serializers import SessionSerializer

# Create your views here.
class SessionApiViewSet(viewsets.ModelViewSet):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer