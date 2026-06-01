from rest_framework import serializers
from .models import *

class LessonsSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Lessons
        fields = '__all__' 


