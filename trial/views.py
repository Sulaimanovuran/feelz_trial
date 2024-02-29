from django.shortcuts import render, redirect
from django.views.decorators.cache import cache_page
from django.http import HttpRequest, HttpResponseForbidden, Http404
from .models import *


from django.shortcuts import render
from .models import Lesson, LessonEnrollment, Lead, Student


even_weekdays = ['tuesday', 'thursday', 'saturday']
odd_weekdays = ['monday', 'wednesday', 'friday']

def lesson_summary(request: HttpRequest):

    lessons = Lesson.objects.prefetch_related('enrollments__lead', 'enrollments__student').order_by('date')

    lesson_summary = {}
    for lesson in lessons:
        date = lesson.date.strftime('%d.%m')  # Group by date in DD.MM format
        day_data = lesson_summary.setdefault(date, {'weekday': lesson.get_weekday_display(), 'date': date, 'lessons': []})

        total_students = 0
        total_leads = 0
        average_age = None
        all_ages = []

        for enrollment in lesson.enrollments.all():
            if enrollment.student:
                total_students += 1
                all_ages.append(enrollment.student.age)
            else:
                total_leads += 1
                all_ages.append(enrollment.lead.age)

        if total_students + total_leads > 0:
            average_age = round(sum(all_ages) / (total_students + total_leads), 1)

        day_data['lessons'].append({
            'id': lesson.id,
            'time': lesson.date.strftime('%H:%M'),
            'level': lesson.level,
            'average_age': average_age,
            'total_students': total_students,
            'total_leads': total_leads
        })

    return render(request, 'index.html', {'lesson_summary': lesson_summary.values()})


def lesson_view(request: HttpRequest, lesson_id: int):
    lesson = Lesson.objects.get(id=lesson_id)
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        age = request.POST.get('age')
        type = request.POST.get('type')
        lvl_type = request.POST.get('lvl-type')
        is_move = request.POST.get('is_move')

        if name:
            if type == 'lead':
                if is_move:
                    last_enroll = LessonEnrollment.objects.filter(lead=is_move).order_by('lesson__date').last()
                    last_enroll.lesson = lesson
                    last_enroll.save()
                else:
                    lead = Lead.objects.create(name=name, phone=phone, age=age)
                    LessonEnrollment.objects.create(lesson_id=lesson_id, lead=lead)
            elif type == 'student':
                student = Student.objects.create(name=name, phone=phone, age=age)
                if lesson.weekday in even_weekdays:
                    all_lessons = Lesson.objects.filter(weekday__in=even_weekdays, 
                                        date__hour=lesson.date.hour, 
                                        date__minute=lesson.date.minute)
                    
                elif lesson.weekday in odd_weekdays:
                    all_lessons = Lesson.objects.filter(weekday__in=odd_weekdays, 
                                        date__hour=lesson.date.hour, 
                                        date__minute=lesson.date.minute)
                    
                if all_lessons:
                    for lesson in all_lessons:
                        
                        enroll = LessonEnrollment.objects.create(lesson_id=lesson.id, student=student)

        elif lvl_type:
            lesson.level=lvl_type
            lesson.save()

        return redirect('lesson_view', lesson_id=lesson_id)

    context = {'students': [], 'leads': [], 'lesson_level': lesson.level}
    enrollments = LessonEnrollment.objects.filter(lesson=lesson_id).prefetch_related('student', 'lead')

    for enroll in enrollments:
        if enroll.lead:
            context['leads'].append(enroll.lead)
        elif enroll.student:
            context['students'].append(enroll.student)

    return render(request, 'lesson.html', {'lesson_info': context, 'lesson_id': lesson_id, 'weekday': lesson.get_weekday_display(), 'date': lesson.date.strftime('%H:%M')})




def delete_lead(request: HttpRequest, lead_id: int, lesson_id: int):

    Lead.objects.get(id=lead_id).delete()
    return redirect('lesson_view', lesson_id=lesson_id)


def move_lead(request: HttpRequest, lead_id: int):

    lessons = Lesson.objects.prefetch_related('enrollments__lead', 'enrollments__student').order_by('date')

    lesson_summary = {}
    for lesson in lessons:
        date = lesson.date.strftime('%d.%m')  # Group by date in DD.MM format
        day_data = lesson_summary.setdefault(date, {'weekday': lesson.get_weekday_display(), 'date': date, 'lessons': []})

        total_students = 0
        total_leads = 0
        average_age = None
        all_ages = []

        for enrollment in lesson.enrollments.all():
            if enrollment.student:
                total_students += 1
                all_ages.append(enrollment.student.age)
            else:
                total_leads += 1
                all_ages.append(enrollment.lead.age)

        if total_students + total_leads > 0:
            average_age = round(sum(all_ages) / (total_students + total_leads), 1)

        day_data['lessons'].append({
            'id': lesson.id,
            'time': lesson.date.strftime('%H:%M'),
            'level': lesson.level,
            'average_age': average_age,
            'total_students': total_students,
            'total_leads': total_leads
        })

    return render(request, 'move.html', {'lesson_summary': lesson_summary.values(), 'lead_id': lead_id})




def moving(request: HttpRequest, lesson_id: int, lead_id: int):
    lesson = Lesson.objects.get(id=lesson_id)
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        age = request.POST.get('age')
        type = request.POST.get('type')
        lvl_type = request.POST.get('lvl-type')

        if name:
            if type == 'lead':
                lead = Lead.objects.create(name=name, phone=phone, age=age)
                LessonEnrollment.objects.create(lesson_id=lesson_id, lead=lead)
            elif type == 'student':
                student = Student.objects.create(name=name, phone=phone, age=age)
                LessonEnrollment.objects.create(lesson_id=lesson_id, student=student)

        elif lvl_type:
            lesson.level=lvl_type
            lesson.save()

        return redirect('lesson_view', lesson_id=lesson_id)

    context = {'students': [], 'leads': [], 'lesson_level': lesson.level}
    enrollments = LessonEnrollment.objects.filter(lesson=lesson_id).prefetch_related('student', 'lead')

    for enroll in enrollments:
        if enroll.lead:
            context['leads'].append(enroll.lead)
        elif enroll.student:
            context['students'].append(enroll.student)

    lead = Lead.objects.get(id=lead_id)
    return render(request, 'moving.html', {'lesson_info': context, 'lesson_id': lesson_id, 'lead': lead})



def delete_student(request: HttpRequest, student_id: int, lesson_id: int):
    enroll = LessonEnrollment.objects.get(student=student_id, lesson=lesson_id).delete()
    return redirect('lesson_view', lesson_id=lesson_id)


def reset_student(request: HttpRequest, student_id: int, lesson_id: int):

    lesson = Lesson.objects.get(id=lesson_id)

    print(lesson_id, student_id)

    if lesson.weekday in even_weekdays:
        all_enrols = LessonEnrollment.objects.filter(lesson__weekday__in=even_weekdays, 
                            lesson__date__hour=lesson.date.hour, 
                            lesson__date__minute=lesson.date.minute, student=student_id)
        
    elif lesson.weekday in odd_weekdays:
        all_enrols = LessonEnrollment.objects.filter(lesson__weekday__in=odd_weekdays, 
                            lesson__date__hour=lesson.date.hour, 
                            lesson__date__minute=lesson.date.minute, student=student_id)
        
    all_enrols.delete()
    
    return redirect('lesson_view', lesson_id=lesson_id)