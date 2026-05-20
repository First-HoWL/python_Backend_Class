from django.db import models

# Create your models here.
class Post(models.Model):
    header = models.CharField(max_length=256)
    content = models.TextField()
    author = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id} | {self.header} by {self.author} at {self.created_at}"
    
class Teacher(models.Model):
    name = models.CharField(max_length=256)
    surname = models.CharField(max_length=256)
    avatar = models.CharField(max_length=256)
    classes_count = models.IntegerField()

    def __str__(self):
        return f"{self.id} | {self.name} {self.surname} and {self.classes_count} classes"
    

class Subject(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return f"{self.id} | {self.name} "

class SubjectToTeacher(models.Model):
    SubjectId = models.IntegerField()
    TeacherId = models.IntegerField()

    def __str__(self):
        return f"{self.id} | {self.SubjectId=} | {self.TeacherId=}"

class Lessons(models.Model):

    class DayChoice(models.TextChoices):
        MONDAY = "Monday", "Monday"
        TUESDAY = "Tuesday", "Tuesday"
        WEDNESDAY = "Wednesday","Wednesday"
        THURSDAY = "Thursday", "Thursday"
        FRIDAY = "Friday", "Friday"
        SATURDAY = "Saturday", "Saturday"
        SUNDAY = "Sunday", "Sunday"

    class LessonStatus(models.TextChoices):
        ACTIVE = "active", "Active"
        CANCELED = "canceled", "Canceled"
    
    class LessonTime(models.TextChoices):
        FIRST = "1", "08:30"
        SECCOND = "2", "11:00"
        THIRD = "3","12:30"
        FOURTH = "4", "14:00"
        
    time = models.TextField(choices=LessonTime.choices)
    SubjectId = models.IntegerField()
    TeacherId = models.IntegerField()
    notes = models.TextField(null=True, blank=True)
    status = models.TextField(choices=LessonStatus.choices)
    day = models.TextField(choices=DayChoice.choices)
    group = models.TextField()

    def __str__(self):
        return f"{self.id} | {self.time} | {self.SubjectId=} | {self.TeacherId=} | {self.notes} | {self.status} | {self.day} | {self.group}"

