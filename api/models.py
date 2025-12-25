from django.db import models
from django.utils import timezone
# Create your models here.
class Section(models.Model):
    name=models.CharField(max_length=40)
    batch=models.IntegerField()
    def __str__(self):
        return f"{self.name}[{self.batch}]"

class Subject(models.Model):
    name=models.CharField(max_length=25)
    section=models.ForeignKey(Section,on_delete=models.CASCADE,related_name='subjects')
    
    def __str__(self):
        return f"{self.name}[{self.section}]"

class Material(models.Model):
    name=models.CharField(max_length=20)
    material=models.FileField(upload_to='uploads/')
    subject=models.ForeignKey(Subject,on_delete=models.CASCADE,related_name='materials')
    upldate=models.DateField(auto_now_add=True)
    def __str__(self):
        return str(self.name)
    
    def delete(self):
        self.material.delete()
        return super().delete()