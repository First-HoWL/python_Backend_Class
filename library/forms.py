from django import forms
from .models import *

def check_banwords(value):
    banwords = ["ban"]
    for banword in banwords:
        if banword in value:
            raise forms.ValidationError("Banwords in the text!!!!")

class PostForm(forms.ModelForm):
    name = forms.CharField(validators=[check_banwords])
    surname = forms.CharField(validators=[check_banwords])
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
    
    