from django.shortcuts import render
from django.shortcuts import redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets

import json
#import requests
#from .forms import *
from .admin import *
from .serializers import *
# Create your views here.

@api_view(['GET']) 
def get_tests(request):
    if request.method == "GET":
        tests = Test.objects.all()
        questionInTest = QuestionInTest.objects.all()
        question = Question.objects.all()
        Tests = []

        for test in tests:
            question_ids = [ qit.question_id for qit in questionInTest if qit.test_id == test.id ]
            testQuestions = [ q for q in question if q.id in question_ids]
            questionsForAnswer = []
            for quest in testQuestions:
                questionsForAnswer.append({
                    "id" : quest.id,
                    "questionId": QuestionInTest.objects.get(test_id=test.id, question_id=quest.id).id,
                    "question": quest.question,
                    "answers": quest.answers,
                    "score": quest.score,
                    "author": AccauntSerializer(Accaunt.objects.get(id=quest.author_id)).data
                })
            t = {
                "id": test.id,
                "author" : AccauntSerializer(Accaunt.objects.get(id=test.author_id)).data,
                "name": test.name,
                "questions": questionsForAnswer #QuestionSerializer(testQuestions, many=True).data
            }
            Tests.append(t)
        return Response(Tests)

