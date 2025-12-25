from rest_framework import serializers
from .models import Subject,Material,Section

class MaterialsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Material
        fields='__all__'

class SubjectsSerializer(serializers.ModelSerializer):
    materials=MaterialsSerializer(many=True)
    class Meta:
        model=Subject
        fields='__all__'

class SectionsSerializer(serializers.ModelSerializer):
    subjects=SubjectsSerializer(many=True)
    class Meta:
        model=Section
        fields='__all__'