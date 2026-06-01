from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Post)
admin.site.register(Teacher)
admin.site.register(Subject)
admin.site.register(SubjectToTeacher)
admin.site.register(Lessons)
admin.site.register(Character)
