from django.contrib import admin
from django.urls import path,include
from .views import Materials,Sections,Register,Addsubject,AddMatrial,Features
urlpatterns = [
    path('materials/', Materials,name='materials'),
    path('', Sections,name='sections'),
    path('register/', Register,name='register'),
    path('addsubject/', Addsubject,name='addsubject'),
    path('addmatrial/', AddMatrial,name='addmatrial'),
    path('features/', Features,name='features'),
]
