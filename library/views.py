from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from datetime import datetime
from django.shortcuts import redirect

from .forms import *
from .admin import *
# Create your views here.

schedule_data = {
    "group": "2024-A",
    "days": {
        "Monday": [
            {
                "lesson_number": 1,
                "time": "08:30",
                "subject": "Physics",
                "teacher": "Class Lenning",
                "notes": "Class lenning ...",
                "status": "active"
            },
            {
                "lesson_number": 2,
                "time": "10:15",
                "subject": "Math",
                "teacher": "Graycleded",
                "notes": "Cancelled lesson",
                "status": "cancelled"
            },
            {
                "lesson_number": 3,
                "time": "11:00",
                "subject": "Physics",
                "teacher": "Class Learning",
                "notes": "Class learning ...",
                "status": "active"
            },
            {
                "lesson_number": 4,
                "time": "13:15",
                "subject": "Physics",
                "teacher": "Today!",
                "notes": "Regular lesson",
                "status": "active"
            }
        ],
        "Tuesday": [
            {
                "lesson_number": 1,
                "time": "08:30",
                "subject": "Physics",
                "teacher": "Emmentest",
                "notes": "Physics class",
                "status": "active"
            },
            {
                "lesson_number": 2,
                "time": "10:15",
                "subject": "History",
                "teacher": "Foday",
                "notes": "History lesson",
                "status": "active"
            },
            {
                "lesson_number": 3,
                "time": "11:00",
                "subject": "History",
                "teacher": "Today",
                "notes": "History lesson",
                "status": "active"
            },
            {
                "lesson_number": 4,
                "time": "13:15",
                "subject": "History",
                "teacher": "Class Irmail",
                "notes": "Regular lesson",
                "status": "active"
            }
        ],
        "Wednesday": [
            {
                "lesson_number": 1,
                "time": "08:30",
                "subject": "Physics",
                "teacher": "Clads Karning",
                "notes": "Physics class",
                "status": "active"
            },
            {
                "lesson_number": 2,
                "time": "10:15",
                "subject": "Wednesday",
                "teacher": "Made Karning",
                "notes": "Special lesson",
                "status": "active"
            },
            {
                "lesson_number": 3,
                "time": "11:00",
                "subject": "Wednesday",
                "teacher": "Made Lerning",
                "notes": "Regular lesson",
                "status": "active"
            },
            {
                "lesson_number": 4,
                "time": "13:15",
                "subject": "History",
                "teacher": "Class Irmail",
                "notes": "History class",
                "status": "active"
            }
        ],
        "Thursday": [
            {
                "lesson_number": 1,
                "time": "08:30",
                "subject": "Math",
                "teacher": "Emntorntest",
                "notes": "Math lesson",
                "status": "active"
            },
            {
                "lesson_number": 2,
                "time": "10:15",
                "subject": "Math",
                "teacher": "Grads Karning",
                "notes": "Math class",
                "status": "active"
            },
            {
                "lesson_number": 3,
                "time": "11:00",
                "subject": "Physics",
                "teacher": "Crade Learning",
                "notes": "Physics lesson",
                "status": "active"
            },
            {
                "lesson_number": 4,
                "time": "13:15",
                "subject": "Physics",
                "teacher": "Fronicentent",
                "notes": "Physics class",
                "status": "active"
            }
        ],
        "Friday": [
            {
                "lesson_number": 1,
                "time": "08:30",
                "subject": "Physics",
                "teacher": "Class Karning",
                "notes": "Physics lesson",
                "status": "active"
            },
            {
                "lesson_number": 2,
                "time": "10:15",
                "subject": "History",
                "teacher": "Class Karning",
                "notes": "History class",
                "status": "active"
            },
            {
                "lesson_number": 3,
                "time": "11:00",
                "subject": "Physics",
                "teacher": "Full Espice",
                "notes": "Physics lesson",
                "status": "active"
            },
            {
                "lesson_number": 4,
                "time": "13:15",
                "subject": "History",
                "teacher": "Class Irmail",
                "notes": "History lesson",
                "status": "active"
            }
        ],
        "Saturday": [],
        "Sunday": [],
    }
}

teachers_data = [
    {
        "id": 1,
        "name": "Dr. Smith",
        "avatar": "teacher_1.png",
        "subjects": [
            "Physics I",
            "Mechanics"
        ],
        "classes_count": 4
    },

    {
        "id": 2,
        "name": "Dr. SI. Food",
        "avatar": "teacher_2.png",
        "subjects": [
            "Physics I",
            "Mechanics",
            "History",
            "Crads"
        ],
        "classes_count": 3
    },

    {
        "id": 3,
        "name": "Dr. Smith",
        "avatar": "teacher_3.png",
        "subjects": [
            "Physics I",
            "Math (Cancellationtest)"
        ],
        "classes_count": 1
    },

    {
        "id": 4,
        "name": "Dr. Hashow",
        "avatar": "teacher_4.png",
        "subjects": [
            "Physics I",
            "Mechanics",
            "Math (Canceled)"
        ],
        "classes_count": 1
    }
]

days_of_week = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday"
]
today = "Monday" #days_of_week[datetime.today().weekday()]


def get_main_page(request):
    context = {
        "today": today
    }
    return render(request, 'library/week_schedule.html', context)


def get_week_schedule(request):
    lessons = Lessons.objects.all()
    print(lessons)
    context = {
        "today": today,
        "schedule": schedule_data
    }
    return render(request, 'library/schedule.html', context)



def get_today_schedule(request):
    context = {
        "today": today,
        "schedule": {
            "group": schedule_data["group"],
            "day": schedule_data["days"][today]
            }
    }
    return render(request, 'library/week_schedule.html', context) # here we need a new day(today) of schedule page

def get_day(request, day):
    if day in days_of_week:
        context = {
            "today": today,
            "current_day": day,
            "schedule": {
                "group": schedule_data["group"],
                "day": schedule_data["days"][day]
                }
        }
        return render(request, 'library/week_schedule.html', context) # here we need a new day of schedule page
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

def get404(request, exception):
    return render(request, 'library/404.html')
