from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class Accaunt(AbstractUser):
    name = models.CharField()
    isTeacher = models.BooleanField(default=False)

    def __str__(self):
        return f"[{self.id}] {self.name} ({self.username})"


class Question(models.Model):
    question = models.TextField()
    answers = models.JSONField(default=list)
    score = models.IntegerField(default=1)
    correctAnswer = models.TextField()
    author = models.ForeignKey(Accaunt, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return f"[{self.id}] Question: {self.question[:50]}"


class Test(models.Model):
    author = models.ForeignKey(Accaunt, on_delete=models.CASCADE)
    name = models.TextField()
    category = models.TextField()
    rating = models.FloatField()

    def __str__(self):
        return f"[{self.id}] Test by {self.author.name}"


class QuestionInTest(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return f"[{self.id}] {self.question.question[:30]} in {self.test}"
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['test', 'question'],
                name='unique_question_in_test'
            )
        ]


class TestCompleted(models.Model):
    accaunt = models.ForeignKey(Accaunt, on_delete=models.CASCADE)
    tests = models.ForeignKey(Test, on_delete=models.CASCADE)
    '''
    
    [
        {
            "questionId": 1,
            "answer": "answer 1"
            "score": 5,
        },
        {
            "questionId": 2,
            "answer": "answer 3"
            "score": 0,
        }
    ]

    '''

    def __str__(self):
        return f"[{self.id}] {self.accaunt.name} completed {self.tests}"
    
class AccountToTestsCompletedQuestions(models.Model):
    testCompleted = models.ForeignKey(TestCompleted, on_delete=models.CASCADE)
    questionId = models.ForeignKey(QuestionInTest, on_delete=models.CASCADE)
    answer = models.TextField()
    score = models.IntegerField(default=0)
