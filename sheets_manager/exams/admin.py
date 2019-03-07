from django.contrib import admin
from .models import User, Exam, Answer, Assesment, Result, Question


admin.register(Exam)
admin.register(Answer)
admin.register(Assesment)
admin.register(Result)
admin.register(Question)