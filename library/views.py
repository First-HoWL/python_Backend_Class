from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
# Create your views here.


def get_portfolio_main(request):

    context = {
        'skills': [
            {"name": "C++", "skill": "intermediate",},
            {"name": "ASP.NET", "skill": "intermediate",},
            {"name": "JavaScript", "skill" : "advanced",},
            {"name": "MySQL", "skill" : "intermediate",},
            {"name": 'docker', "skill": "intermediate",},
            {"name": 'python', "skill": "invalid",},
        ]
    }
    return render(request, 'library/main.html', context)

def get_projects_main(request):
    context = {
        'projects': [
            {"name": "PixelRun", "desc": "PixelRun is a platformer game", "year": "2025", "skills":{
                "C++", "SFML", "ASP.NET", "MySQL", "React", "JavaScript"
            } },
            {"name": "Tournaments", "desc": "Tournaments is a web-site for people who want to hold a tournament", "year": "2025", "skills":{
                "ASP.NET", "MySQL", "React", "JavaScript"
            } },
        ]
    }
    return render(request, 'library/projects.html', context)

def get_contacts_main(request):
    context = {
        'email' : "example@example.com",
        'phone' : "0951234567"
    }
    return render(request, 'library/contacts.html', context)

