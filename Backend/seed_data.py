"""
Скрипт для заполнения БД тестовыми данными.

Запуск:
    python manage.py shell < seed_data.py

Или так:
    python manage.py shell
    >>> exec(open('seed_data.py').read())
"""

import json
from django.contrib.auth.hashers import make_password
from library.models import Accaunt, Test, Question, QuestionInTest, TestCompleted, AccountToTestsCompletedQuestions

# ─────────────────────────────────────────────
# 1. ОЧИСТКА (опционально — раскомментируй если нужно начать с чистого листа)
# ─────────────────────────────────────────────
# AccountToTestsCompletedQuestions.objects.all().delete()
# TestCompleted.objects.all().delete()
# QuestionInTest.objects.all().delete()
# Question.objects.all().delete()
# Test.objects.all().delete()
# Accaunt.objects.exclude(is_superuser=True).delete()

# ─────────────────────────────────────────────
# 2. ПОЛЬЗОВАТЕЛИ
# ─────────────────────────────────────────────

teacher, _ = Accaunt.objects.get_or_create(
    username="teacher1",
    defaults={
        "password": make_password("teacher123"),
        "name": "Олена Іванівна",
        "isTeacher": True,
    }
)
print(f"[+] Teacher: {teacher.username} (id={teacher.id})")

student, _ = Accaunt.objects.get_or_create(
    username="student1",
    defaults={
        "password": make_password("student123"),
        "name": "Іван Петров",
        "isTeacher": False,
    }
)
print(f"[+] Student: {student.username} (id={student.id})")

# ─────────────────────────────────────────────
# 3. ТЕСТЫ
# ─────────────────────────────────────────────

test1, _ = Test.objects.get_or_create(
    name="Математика — Базовий рівень",
    defaults={
        "category": "Математика",
        "rating": 0,
        "author": teacher,
    }
)
print(f"[+] Test: {test1.name} (id={test1.id})")

test2, _ = Test.objects.get_or_create(
    name="Загальні знання",
    defaults={
        "category": "Загальне",
        "rating": 0,
        "author": teacher,
    }
)
print(f"[+] Test: {test2.name} (id={test2.id})")

# ─────────────────────────────────────────────
# 4. ВОПРОСЫ
# ─────────────────────────────────────────────

questions_math = [
    {
        "question": "Скільки буде 2 + 2?",
        "answers": ["3", "4", "5", "6"],
        "correctAnswer": "4",
        "score": 10,
    },
    {
        "question": "Скільки буде 5 × 6?",
        "answers": ["28", "30", "32", "36"],
        "correctAnswer": "30",
        "score": 10,
    },
    {
        "question": "Корінь квадратний з 81?",
        "answers": ["7", "8", "9", "11"],
        "correctAnswer": "9",
        "score": 15,
    },
    {
        "question": "Скільки буде 100 ÷ 4?",
        "answers": ["20", "25", "30", "40"],
        "correctAnswer": "25",
        "score": 10,
    },
    {
        "question": "Яке число є простим?",
        "answers": ["4", "6", "9", "7"],
        "correctAnswer": "7",
        "score": 15,
    },
]

questions_general = [
    {
        "question": "Яка столиця України?",
        "answers": ["Львів", "Харків", "Київ", "Одеса"],
        "correctAnswer": "Київ",
        "score": 10,
    },
    {
        "question": "Скільки місяців у році?",
        "answers": ["10", "11", "12", "13"],
        "correctAnswer": "12",
        "score": 5,
    },
    {
        "question": "Яка найбільша планета Сонячної системи?",
        "answers": ["Земля", "Сатурн", "Юпітер", "Нептун"],
        "correctAnswer": "Юпітер",
        "score": 10,
    },
    {
        "question": "Хто написав 'Кобзар'?",
        "answers": ["Іван Франко", "Леся Українка", "Тарас Шевченко", "Микола Гоголь"],
        "correctAnswer": "Тарас Шевченко",
        "score": 10,
    },
    {
        "question": "Скільки сторін у трикутника?",
        "answers": ["2", "3", "4", "5"],
        "correctAnswer": "3",
        "score": 5,
    },
]

def create_questions(questions_data, test, author):
    for q_data in questions_data:
        q, created = Question.objects.get_or_create(
            question=q_data["question"],
            defaults={
                "answers": q_data["answers"],
                "correctAnswer": q_data["correctAnswer"],
                "score": q_data["score"],
                "author": author,
            }
        )
        # Привязка вопроса к тесту
        qit, _ = QuestionInTest.objects.get_or_create(test=test, question=q)
        status_str = "создан" if created else "уже существует"
        print(f"    [q] '{q.question[:40]}' ({status_str})")

print(f"\n[+] Вопросы для теста: {test1.name}")
create_questions(questions_math, test1, teacher)

print(f"\n[+] Вопросы для теста: {test2.name}")
create_questions(questions_general, test2, teacher)

# ─────────────────────────────────────────────
# 5. ТЕСТОВАЯ СЕССИЯ (студент проходит тест1)
# ─────────────────────────────────────────────

session = TestCompleted.objects.create(
    accaount=student,
    tests=test1
)
print(f"\n[+] Сессия создана (id={session.id}) — студент {student.username} проходит тест '{test1.name}'")

# Студент отвечает на все вопросы теста
for qit in QuestionInTest.objects.filter(test=test1):
    q = qit.question
    # Студент всегда отвечает правильно (для демо)
    answer = q.correctAnswer
    score = q.score

    AccountToTestsCompletedQuestions.objects.create(
        testCompleted=session,
        questionId=qit,
        answer=answer,
        score=score
    )
    print(f"    [a] '{q.question[:40]}' → '{answer}' ({score} очков)")

total = sum(
    AccountToTestsCompletedQuestions.objects
    .filter(testCompleted=session)
    .values_list('score', flat=True)
)
print(f"\n[✓] Готово! Итоговый счёт студента: {total} очков")
print(f"\n    Логины для проверки API:")
print(f"    Учитель  — login: teacher1 / password: teacher123")
print(f"    Студент  — login: student1 / password: student123")
print(f"    Session ID для /get_test_result/: accauntId={student.id}, sessionId={session.id}")
