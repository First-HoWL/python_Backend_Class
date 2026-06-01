from django.db import models
import random


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

class Character(models.Model):
    name = models.TextField()
    hp = models.FloatField()
    attack = models.FloatField()
    defense = models.FloatField()

    def __str__(self):
        return f"{self.id} | {self.name} | {self.hp} hp | {self.attack=} | {self.defense=}"
    

    
    @property
    def hp_(self):
        return self.hp

    @hp_.setter
    def hp_(self, value):
        if value < 0:
            self.hp = 0
        else:
            self.hp = round(value, 3)

    def take_damage(self, damage):
        new_damage = damage - min((damage * (self.defense / 100)), damage)
        self.hp_ -= new_damage
        return new_damage

    def attack_char(self, other):
        if self.is_alive:
            damage_modify = self.attack + self.attack * (random.randint(-20, 20) / 100)
            responce = other.take_damage(damage_modify)
            if responce != -1:
                return responce
            else:
                return -1
        else:
            return 0

    @property
    def is_alive(self):
        return self.hp_ > 0