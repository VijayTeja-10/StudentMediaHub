from django.shortcuts import render
from rest_framework import generics
from .models import Subject,Section
from .serializers import SubjectsSerializer,SectionsSerializer

# Create your views here.

class SubjectsView(generics.ListAPIView):
    queryset=Subject.objects.all()
    serializer_class=SubjectsSerializer

class SectionsView(generics.ListAPIView):
    queryset=Section.objects.all()
    serializer_class=SectionsSerializer