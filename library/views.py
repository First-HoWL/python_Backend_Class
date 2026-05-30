from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from datetime import datetime
from django.shortcuts import redirect

import json
import requests
from .forms import *
from .admin import *
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

def get404(request, exception):
    return render(request, 'library/404.html')
