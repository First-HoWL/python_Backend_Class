from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from datetime import datetime
from django.shortcuts import redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets

import json
import requests
from .forms import *
from .admin import *
from .serializers import *
# Create your views here.

days_of_week = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday"
]
today = days_of_week[datetime.today().weekday()]

lesson_time = {
    "1" : "08:30",
    "2" : "11:00",
    "3" : "12:30",
    "4" : "14:00"
}



def get_main_page(request):
    context = {
        "today": today
    }
    return render(request, 'library/week_schedule.html', context)


def get_week_schedule(request):
    teachers = Teacher.objects.all()
    subjects = Subject.objects.all()
    lessons = Lessons.objects.all()
    days = {
        "Monday": [],
        "Tuesday": [],
        "Wednesday": [],
        "Thursday": [],
        "Friday": [],
        "Saturday": [],
        "Sunday": []
    }

    for lesson in lessons:
        days[lesson.day].append({
            "time": lesson_time[lesson.time], 
            "subject": subjects.filter(id = lesson.SubjectId).first().name,
            "teacher": teachers.filter(id = lesson.TeacherId).first().name,
            "notes": lesson.notes,
            "status": lesson.status
        })

    # print(lessons)
    context = {
        "today": today,
        "schedule": {
            "days": days
            }
    }
    return render(request, 'library/schedule.html', context)



def get_today_schedule(request):
    teachers = Teacher.objects.all()
    subjects = Subject.objects.all()
    lessons = Lessons.objects.all()
    days = {
        "Monday": [],
        "Tuesday": [],
        "Wednesday": [],
        "Thursday": [],
        "Friday": [],
        "Saturday": [],
        "Sunday": []
    }

    for lesson in lessons:
        days[lesson.day].append({
            "time": lesson_time[lesson.time], 
            "subject": subjects.filter(id = lesson.SubjectId).first().name,
            "teacher": teachers.filter(id = lesson.TeacherId).first().name,
            "notes": lesson.notes,
            "status": lesson.status
        })

    context = {
        "today": today,
        "schedule": {
            "day": days[today]
            }
    }
    return render(request, 'library/schedule_one_day.html', context) 

def get_day(request, day):

    teachers = Teacher.objects.all()
    subjects = Subject.objects.all()
    lessons = Lessons.objects.all()
    days = {
        "Monday": [],
        "Tuesday": [],
        "Wednesday": [],
        "Thursday": [],
        "Friday": [],
        "Saturday": [],
        "Sunday": []
    }

    for lesson in lessons:
        days[lesson.day].append({
            "time": lesson_time[lesson.time], 
            "subject": subjects.filter(id = lesson.SubjectId).first().name,
            "teacher": teachers.filter(id = lesson.TeacherId).first().name,
            "notes": lesson.notes,
            "status": lesson.status
        })



    if day in days_of_week:
        context = {
            "today": today,
            "current_day": day,
            "schedule": {
                "day": days[day]
                }
        }
        return render(request, 'library/schedule_one_day.html', context) 
    else:
        return render(request, 'library/404.html')

def get_teachers(request):
    teachers = Teacher.objects.all()
    subjects = Subject.objects.all()
    subjectToTeacher = SubjectToTeacher.objects.all()
    context = {
        "teachers": []
    }
    for teacher in teachers:
        subjectsTeachers = subjectToTeacher.filter(TeacherId=teacher.id)
        curr_subjects = []
        for sub_id in subjectsTeachers:
            curr_subjects.append({
                "id": subjects.filter(id=sub_id.SubjectId)[0].id,
                "name": subjects.filter(id=sub_id.SubjectId)[0].name
                })
        context["teachers"].append({
            "name" : teacher.name,
            "surname" : teacher.surname,
            "avatar": teacher.avatar,
            "classes_count": teacher.classes_count,
            "subjects": curr_subjects
        })

    
    return render(request, 'library/teachers.html', context)

def teachers_add(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = PostForm()
    
    return render(request, "library/add_teacher.html", {'form': form})

percents_per_month = {
    "3": 8.,
    "4": 8.4,
    "5": 8.5,
    "6": 8.8,
    "7": 9.1,
    "8": 9.4,
    "9": 9.8,
    "10": 10.2,
    "11": 10.6,
    "12": 11.,
    "13": 11.,
    "14": 11.,
    "15": 11.,
    "16": 11.,
    "17": 11.,
    "18": 11.,
    "19": 11.,
    "20": 11.,
    "21": 11.,
    "22": 11.,
    "23": 11.,
    "24": 11.,
}

def deposit(request):
    if request.method == 'POST':
        form = deposit_calculator(request.POST)
        if form.is_valid():
            money = max(float(form.data['count']), 0)
            term = min(int(form.data['term']), 24)
            percents = percents_per_month[str(term)]
            
            final_money = money

            if form.data.__contains__('is_add_percents'):
                final_money = round(money * ((1 + (percents / 1200)) **  term), 2)
            else: 
                final_money = round(money * ((1 + (percents / 1200) *  term) ), 2)
                

            
            tax = round((final_money - money) * 0.23, 2)

            final_money_with_tax = round(final_money - tax, 2)  

            context = {
                'form': form, 
                'request': {
                    "start_money": money,
                    "final_money_without_tax" : final_money,
                    "money": final_money_with_tax,
                    "percent" : percents,
                    "tax" : tax
                    }
                }
            return render(request, "library/deposit.html",context )
    else:
        form = deposit_calculator()

    return render(request, "library/deposit.html", {'form': form})

def get_catalog(request):

    response = requests.get('https://fakestoreapi.com/products')
    
    context = {
        "response" : response.json()
    }

    return render(request, 'library/catalog.html', context)

def get_cart(request):
    response = requests.get('https://fakestoreapi.com/products')
    
    context = {
        "response" : [],
    }

    card = request.session.get("card", [])
    print("cart:")
    print(card)
    for card_el in card:
        ellem = next((x for x in response.json() if int(x["id"]) == int(card_el["id"])), None)
        print(ellem)
        if ellem:
            context["response"].append(
                    { 
                        "product" : ellem, 
                        "count" : card_el["count"]
                    }
                )

    
    return render(request, 'library/cart.html', context)

def get_product(request, id):
    response = requests.get(f'https://fakestoreapi.com/products/{id}')

    #print(response.json())
    context = {
        "product" : response.json()
    }

    if request.method == "GET":
        checked = request.session.get("checked", [])
        print(checked)
        context["checked"] = id in checked
        if id not in checked:
            checked.append(id)
        request.session["checked"] = checked
        request.session.modified = True

        add_to_cart = request.GET.get("add_to_cart")
        if add_to_cart:
            card = request.session.get("card", [])

            product = next((x for x in card if x["id"] == add_to_cart), None)
            print(card)
            if not product:
                card.append({
                    "id": add_to_cart,
                    "count": 1
                })
            else:
                product["count"] += 1

            request.session['card'] = card
            request.session.modified = True

    return render(request, 'library/one_product.html', context)


@api_view(['GET', 'POST'])
def lesson(request):
    if request.method == "GET":
        lessons = Lessons.objects.all()
        serializer = LessonsSerializer(lessons, many=True)
        return Response(serializer.data)
    if request.method == "POST":
        serializer = LessonsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE', 'PUT'])
def the_lesson(request, pk):
    lesson = Lessons.objects.get(pk=pk)
    if request.method == 'DELETE':
        lesson.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    if request.method == 'PUT':
        serializer = LessonsSerializer(lesson, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def get404(request, exception):
    return render(request, 'library/404.html')
