from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from django.db.models import Sum
from django.contrib.auth.hashers import make_password, check_password
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

import json
#import requests
#from .forms import *
from .admin import *
from .serializers import *
# Create your views here.

import random

def get_accaunt_id_from_token(request):
    auth_header = request.headers.get("Authorization")
	
    if not auth_header:
        return None, "Authorization header is required, aboba"

    parts = auth_header.split()

    if len(parts) != 2:
        return None, "Invalid Authorization header"

    if parts[0].lower() != "bearer":
        return None, "Authorization header must start with Bearer"

    token = parts[1]

    try:
        payload = AccessToken(token)
    except (InvalidToken, TokenError):
        return None, "Invalid or expired token"

    accaunt_id = payload.get("accaunt_id")

    if accaunt_id is None:
        return None, "accaunt_id not found in token"

    return accaunt_id, None

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
                "category": test.category,
                "rating": test.rating,
                "author" : AccauntSerializer(Accaunt.objects.get(id=test.author_id)).data,
                "name": test.name,
                "questions": questionsForAnswer 
            }
            Tests.append(t)
        return Response(Tests)

@api_view(['POST'])
def answer_question(request):
    data = request.data

    required_fields = [
        'sessionId',
        'questionId',
        'answer'
    ]

    accaunt_id, error = get_accaunt_id_from_token(request)

    if error:
        return Response(
            {"error": error},
            status=status.HTTP_401_UNAUTHORIZED
        )


    for field in required_fields:
        if field not in data:
            return Response(
                {"error": f"Field '{field}' is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

    try:
        accaunt = Accaunt.objects.get(id=accaunt_id)
        test_completed = TestCompleted.objects.get(id=data['sessionId'])
        question_in_test = QuestionInTest.objects.get(id=data['questionId'])

    except Accaunt.DoesNotExist:
        return Response(
            {"error": "Account not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    except TestCompleted.DoesNotExist:
        return Response(
            {"error": "Session not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    except QuestionInTest.DoesNotExist:
        return Response(
            {"error": "Question not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    if test_completed.accaunt_id != accaunt.id:
        return Response(
            {"error": "This session does not belong to this account"},
            status=status.HTTP_403_FORBIDDEN
        )

    question = question_in_test.question
    answer = str(data['answer']).strip()

    if AccountToTestsCompletedQuestions.objects.filter(
        testCompleted=test_completed,
        questionId=question_in_test
    ).exists():
        return Response(
            {"error": "Question already answered"},
            status=status.HTTP_400_BAD_REQUEST
        )

    score = 0
    is_correct = False

    if answer == question.correctAnswer:
        score = question.score
        is_correct = True

    AccountToTestsCompletedQuestions.objects.create(
        testCompleted=test_completed,
        questionId=question_in_test,
        answer=answer,
        score=score
    )

    return Response(
        {
            "isCorrect": is_correct,
            "score": score,
            "correctAnswer": question.correctAnswer
        },
        status=status.HTTP_201_CREATED
    )

@api_view(['GET'])
def get_test_result(request, accauntId, sessionId):

    try:
        accaunt = Accaunt.objects.get(id=accauntId)
    except Accaunt.DoesNotExist:
        return Response(
            {"error": "Account not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    try:
        test_completed = TestCompleted.objects.get(id=sessionId)
    except TestCompleted.DoesNotExist:
        return Response(
            {"error": "Session not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    if test_completed.accaunt_id != accaunt.id:
        return Response(
            {"error": "This session does not belong to this account"},
            status=status.HTTP_403_FORBIDDEN
        )

    total_score = (
        AccountToTestsCompletedQuestions.objects
        .filter(testCompleted=test_completed)
        .aggregate(total=Sum('score'))
    )['total'] or 0

    test = test_completed.tests

    test_data = {
        "id": test.id,
        "category": test.category,
        "rating": test.rating,
        "author": AccauntSerializer(test.author).data,
        "name": test.name,
    }

    questions_for_test = []

    question_in_tests = (
        QuestionInTest.objects
        .filter(test=test)
        .select_related('question', 'question__author')
    )

    for qit in question_in_tests:
        question = qit.question

        user_answer_obj = (
            AccountToTestsCompletedQuestions.objects
            .filter(
                testCompleted=test_completed,
                questionId=qit
            )
            .first()
        )

        questions_for_test.append({
            "id": question.id,
            "questionId": qit.id,  # id записи QuestionInTest
            "question": question.question,
            "answers": question.answers,
            "correctAnswer": question.correctAnswer,
            "userAnswered": (
                user_answer_obj.answer
                if user_answer_obj else None
            ),
            "score": question.score,
            "author": AccauntSerializer(question.author).data
        })

    context = {
        "score": total_score,
        "test": test_data,
        "questions": questions_for_test
    }

    return Response(
        context,
        status=status.HTTP_200_OK
    )

@api_view(['POST'])
def create_session(request):
    data = request.data

    accaunt_id, error = get_accaunt_id_from_token(request)

    if error:
        return Response(
            {"error": error},
            status=status.HTTP_401_UNAUTHORIZED
        )


    try:
        accaunt = Accaunt.objects.get(id=accaunt_id)
        test = Test.objects.get(id=data['testId'])
    except Accaunt.DoesNotExist:
        return Response(
            {"error": "Account not found"},
            status=status.HTTP_404_NOT_FOUND
        )
    
    session = TestCompleted.objects.create(
        accaount=accaunt, 
        tests=test
    )
    return Response(
        {"sessionId": session.id},
        status=status.HTTP_201_CREATED
    )

@api_view(['POST'])
def create_accaunt(request):
    data = request.data

    required_fields = [
        'login',
        'password',
        'name'
    ]

    for field in required_fields:
        if field not in data:
            return Response(
                {"error": f"Field '{field}' is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

    login = str(data['login']).strip()
    password = str(data['password'])
    name = str(data['name']).strip()

    if len(login) < 3:
        return Response(
            {"error": "Login must contain at least 3 characters"},
            status=status.HTTP_400_BAD_REQUEST
        )

    if len(password) < 6:
        return Response(
            {"error": "Password must contain at least 6 characters"},
            status=status.HTTP_400_BAD_REQUEST
        )

    if Accaunt.objects.filter(username=login).exists():
        return Response(
            {"error": "Login already exists"},
            status=status.HTTP_409_CONFLICT
        )

    accaunt = Accaunt.objects.create(
        username=login,
        password=make_password(password),
        name=name
    )

    return Response(
        {
            "success": True,
            "accaunt": {
                "id": accaunt.id,
                "login": accaunt.username,
                "name": accaunt.name,
                "isTeacher": accaunt.isTeacher
            }
        },
        status=status.HTTP_201_CREATED
    )

@api_view(['POST'])
def create_question(request):
    data = request.data

    required_fields = [
        'question',
        'answers',
        'score',
        'correctAnswer'
    ]

    for field in required_fields:
        if field not in data:
            return Response(
                {"error": f"Field '{field}' is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
    accaunt_id, error = get_accaunt_id_from_token(request)
    
    if error:
        return Response(
            {"error": error},
            status=status.HTTP_401_UNAUTHORIZED
        )

    question = str(data['question']).strip()
    answers = str(data['answers'])
    correctAnswer = str(data['correctAnswer'])
    score = int(data['score'])
    

    question = Question.objects.create(
        question=question,
        answers=answers,
        score=score,
        correctAnswer=correctAnswer,
        author = Accaunt.objects.get(id=accaunt_id)
    )

    return Response(
        {
            "success": True,
            "question": {
                "question": question.question,
                "answers": question.answers,
                "score": question.score,
                "correctAnswer": question.correctAnswer
            }
        },
        status=status.HTTP_201_CREATED
    )

@api_view(['POST'])
def create_test(request):
    data = request.data

    required_fields = [
        'name',
        'category'
    ]

    for field in required_fields:
        if field not in data:
            return Response(
                {"error": f"Field '{field}' is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
    accaunt_id, error = get_accaunt_id_from_token(request)
    
    if error:
        return Response(
            {"error": error},
            status=status.HTTP_401_UNAUTHORIZED
        )

    name = str(data['name']).strip()
    category = str(data['category']).strip()

    test = Question.objects.create(
        name=name,
        category=category,
        author = Accaunt.objects.get(id=accaunt_id),
        rating=(random.randint(300, 500) /100)
    )

    return Response(
        {
            "success": True,
            "test": {
                "name": test.name,
                "category": test.category,
                "rating": test.rating
            }
        },
        status=status.HTTP_201_CREATED
    )

@api_view(['POST'])
def add_questions_to_test(request):
    data = request.data

    required_fields = [
        'questionsIds', # [2, 4, 1]
        'testId'
    ]

    for field in required_fields:
        if field not in data:
            return Response(
                {"error": f"Field '{field}' is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
    accaunt_id, error = get_accaunt_id_from_token(request)
    
    if error:
        return Response(
            {"error": error},
            status=status.HTTP_401_UNAUTHORIZED
        )

    questions = data['questionsIds']

    testId = int(data['testId'])
    
    test = get_object_or_404(Test, id=testId)

    if test.author_id != accaunt_id:
        return Response(
            {"error": "Test doesn`t belong to you!"},
            status=status.HTTP_403_FORBIDDEN
        )



    test = Test.objects.get(id=testId)

    for question_id in questions:
        question = Question.objects.get(id=question_id)

        QuestionInTest.objects.create(
            test=test,
            question=question
        )

    return Response(
        {
            "success": True,
            "testId": testId
        },
        status=status.HTTP_201_CREATED
    )


@api_view(['POST'])
def login_accaunt(request):
    data = request.data

    required_fields = [
        'login',
        'password'
    ]

    for field in required_fields:
        if field not in data:
            return Response(
                {"error": f"Field '{field}' is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

    login = str(data['login']).strip()
    password = str(data['password'])

    try:
        accaunt = Accaunt.objects.get(username=login)
    except Accaunt.DoesNotExist:
        return Response(
            {"error": "Invalid login or password"},
            status=status.HTTP_401_UNAUTHORIZED
        )

    if not check_password(password, accaunt.password):
        return Response(
            {"error": "Invalid login or password"},
            status=status.HTTP_401_UNAUTHORIZED
        )

    refresh = RefreshToken()

    refresh["accaunt_id"] = accaunt.id
    refresh["username"] = accaunt.username
    refresh["isTeacher"] = accaunt.isTeacher

    return Response(
        {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "success": True,
            "accaunt": {
                "id": accaunt.id,
                "login": accaunt.username,
                "name": accaunt.name,
                "isTeacher": accaunt.isTeacher
            }
        },
        status=status.HTTP_200_OK
    )