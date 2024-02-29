from django.db import models

class Lead(models.Model):
    name = models.CharField(max_length=250, verbose_name="Имя", null=True, blank=True)
    phone = models.CharField(max_length=255, verbose_name="Сделка", null=True, blank=True)
    age = models.IntegerField(verbose_name="Возраст", null=True, blank=True)

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name = "Лид"
        verbose_name_plural = "Лиды"


class Student(models.Model):
    name = models.CharField(max_length=250, verbose_name="Имя", null=True, blank=True)
    phone = models.CharField(max_length=255, verbose_name="Сделка", null=True, blank=True)
    age = models.IntegerField(verbose_name="Возраст", null=True, blank=True)

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name = "Студент"
        verbose_name_plural = "Студенты"


class Lesson(models.Model):

    LEVELS = [
        ("start", "Starter"),
        ("pre-begin", "Pre Beginner"),
        ("begin", "Beginner"),
        ("element", "Elementary"),
        ("pre-inter", "Pre Intermediate"),
        ("inter", "Intermediate"),
        ("up-inter", "Upper Intermediate"),
        ("advanc", "Advanced")
    ]
    WEEKDAYS = [
        ("monday", "Понедельник"),
        ("tuesday", "Вторник"),
        ("wednesday", "Среда"),
        ("thursday", "Четверг"),
        ("friday", "Пятница"),
        ("saturday", "Суббота")
    ]

    date = models.DateTimeField(verbose_name="Дата", null=True, blank=True)
    level = models.CharField(max_length=30, choices=LEVELS, null=True, blank=True, verbose_name="Уровень")
    weekday = models.CharField(max_length=30, choices=WEEKDAYS, null=True, blank=True, verbose_name="День недели")

    def __str__(self) -> str:
        if self.date:
            formatted_date = self.date.strftime("%d.%m.%y")
            formatted_time = self.date.strftime("%H:%M")
            return f"{formatted_date} | {formatted_time}  |  {self.level}"
        else:
            return "No date"
        

class LessonEnrollment(models.Model):

    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name="Урок", related_name="enrollments")
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, verbose_name="Лид", related_name="enrollments", null=True, blank=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name="Студент", related_name="enrollments", null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.lesson}  |  {self.lead.name if self.lead else self.student.name}"

