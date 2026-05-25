from django import forms
from .models import *


class PostForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['name', 'surname', 'avatar', 'classes_count']
        labels = {'name': "Name", 
                  'surname': "Surname", 
                  'avatar': "Teacher`s avatar", 
                  'classes_count': "Teacher`s classes"}
        error_messages = {
            'name':{
                "required" : "Can`t be null",
                "max_length" : "Not more than 256 characters"
            },
            'surname':{
                "required" : "Can`t be null",
                "max_length" : "Not more than 256 characters"
            },
            'avatar':{
                "required" : "Can`t be null",
                "max_length" : "Not more than 256 characters"
            },
            'classes_count':{
                "required" : "Can`t be null"
            },
        }
    