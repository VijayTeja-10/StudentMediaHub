from django.contrib import admin
from .models import Subject,Material,Section
# Register your models here.
admin.site.register(Section)
admin.site.register(Subject)
admin.site.register(Material)