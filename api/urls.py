from django.contrib import admin
from django.urls import path,include
from .views import SubjectsView,SectionsView
urlpatterns = [
    path('subjects/', SubjectsView.as_view()),
    path('sections/', SectionsView.as_view()),
]
