from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
# Create your views here.

products = [
    {
        "id": 1,
        "name": "AMD Ryzen 7 7800X3D",
        "description": "Потужний 8-ядерний процесор для ігор та роботи.",
        "image": "",
        "url": "https://hard.rozetka.com.ua/ua/391959990/p391959990/",
        "price": 17872
    },
    {
        "id": 2,
        "name": "NVIDIA GeForce RTX 4070 Super",
        "description": "Сучасна відеокарта для геймінгу у 2K та 4K.",
        "image": "",
        "url": "https://rozetka.com.ua/ua/search/?text=RTX+4070+Super",
        "price": 32999
    },
    {
        "id": 3,
        "name": "Kingston Fury Beast DDR5 32GB",
        "description": "Оперативна пам’ять DDR5 32 ГБ (2x16 ГБ) 6000MHz.",
        "image": "",
        "url": "https://rozetka.com.ua/ua/search/?text=Kingston+Fury+Beast+DDR5+32GB",
        "price": 5499
    },
    {
        "id": 4,
        "name": "Samsung 990 PRO 1TB",
        "description": "NVMe SSD накопичувач об’ємом 1 ТБ.",
        "image": "",
        "url": "https://rozetka.com.ua/ua/search/?text=Samsung+990+PRO+1TB",
        "price": 4799
    },
    {
        "id": 5,
        "name": "MSI MAG B650 Tomahawk WiFi",
        "description": "Материнська плата для процесорів AMD AM5.",
        "image": "",
        "url": "https://rozetka.com.ua/ua/search/?text=MSI+MAG+B650+Tomahawk+WiFi",
        "price": 8999
    },
    {
        "id": 6,
        "name": "Deepcool AK620",
        "description": "Потужне охолодження для процесора.",
        "image": "",
        "url": "https://rozetka.com.ua/ua/search/?text=Deepcool+AK620",
        "price": 2599
    },
    {
        "id": 7,
        "name": "Corsair RM850x",
        "description": "Блок живлення 850W з сертифікацією 80+ Gold.",
        "image": "",
        "url": "https://rozetka.com.ua/ua/search/?text=Corsair+RM850x",
        "price": 6499
    }
]


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

def fibonacci_up_to(n):
    i = 0
    a, b = 0, 1
    while i < n:
        yield a
        a, b = b, a + b
        i += 1

def get_fibonacci(request, num = None):
    amount = request.GET.get('amount')
    context = {
        "fibonacci": [],
    }
    if num is None and amount is None:
        for fib in fibonacci_up_to(10):
            context["fibonacci"].append(fib)
    elif num is None and not amount is None:
        for fib in fibonacci_up_to(min(int(amount), 200)):
            context["fibonacci"].append(fib)
    elif not num is None and amount is None:
        i = 0
        for fib in fibonacci_up_to(num + 1):
            if i is num:
                context["fibonacci"].append(fib)
            i += 1

    return render(request, 'library/fibonacci.html', context)

def get_catalog(request):
    context = {
        "products": products
    }
    return render(request, 'library/catalog.html', context)

def get_product_page(request, id):
    context = {
        "product": products.sort(key=lambda x: x["id"] is id)
    }
    return render(request, 'library/catalog.html', context)

