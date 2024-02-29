from django.urls import path, include

from .views import *

urlpatterns = [
    path('', lesson_summary, name='home'),
    path('lesson/<int:lesson_id>', lesson_view, name='lesson_view'),
    path('delete_lead/<int:lead_id>/<int:lesson_id>/', delete_lead, name='delete_lead'),
    path('move_lead/<int:lead_id>', move_lead, name='move_lead'),
    path('lesson/move/<int:lesson_id>/<int:lead_id>', moving, name='moving'),
    path('delete_student/<int:student_id>/<int:lesson_id>/', delete_student, name='delete_student'),
    path('reset_student/<int:student_id>/<int:lesson_id>/', reset_student, name='reset_student'),
]
