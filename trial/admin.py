from django.contrib import admin

from .models import *


admin.site.register(Lead)
admin.site.register(Student)
admin.site.register(Lesson)
admin.site.register(LessonEnrollment)