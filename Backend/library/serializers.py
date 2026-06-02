from rest_framework import serializers
from .models import *

class AccauntSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    isTeacher = serializers.IntegerField(read_only=True)
    password = serializers.CharField(write_only=True)
    login = serializers.CharField(write_only=True)

    class Meta:
        model  = Accaunt
        fields = ['id', 'login', 'password', 'name', 'isTeacher']

class QuestionSerializer(serializers.ModelSerializer):

    correctAnswer = serializers.CharField(write_only=True)

    class Meta:
        model  = Question
        fields = '__all__'


# class CharacterSerializer(serializers.ModelSerializer):
#     class Meta:
#         model  = Character
#         fields = '__all__'
    
#     def validate_hp(self, value):
#         if value <= 0:
#             raise serializers.ValidationError("HP must be a positive integer.")
#         return value
    
#     def validate_attack(self, value):
#         if value <= 0:
#             raise serializers.ValidationError("Attack must be a non-negative integer.")
#         return value
    
#     def validate_defense(self, value):
#         if value <= 0:
#             raise serializers.ValidationError("Defense must be a non-negative integer.")
#         return value