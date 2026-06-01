from rest_framework import serializers
from .models import *

class LessonsSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Lessons
        fields = '__all__' 


class CharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Character
        fields = '__all__'
    
    def validate_hp(self, value):
        if value <= 0:
            raise serializers.ValidationError("HP must be a positive integer.")
        return value
    
    def validate_attack(self, value):
        if value <= 0:
            raise serializers.ValidationError("Attack must be a non-negative integer.")
        return value
    
    def validate_defense(self, value):
        if value <= 0:
            raise serializers.ValidationError("Defense must be a non-negative integer.")
        return value