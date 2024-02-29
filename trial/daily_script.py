
from datetime import datetime, timedelta
from .models import Lesson

# Расписание занятий
schedule = [
    "08:00",
    "09:10",
    "10:20",
    "11:30",
    "12:40",
    "13:50",
    "15:00",
    "16:10",
    "17:20",
    "18:30",
    "19:40"
]

# Дни недели
weekdays = [
    "monday",
    "tuesday",
    "wednesday",
    "thursday",
    "friday",
    "saturday"
]

# Текущая дата
start_date = datetime.now()

# Создаем занятия на месяц вперед
for day in range(30):
    date = start_date + timedelta(days=day)
    if date.strftime('%A').lower() not in weekdays:
        continue
    for time in schedule:
        hour, minute = map(int, time.split(':'))
        lesson_time = date.replace(hour=hour, minute=minute)
        lesson = Lesson(date=lesson_time, weekday=date.strftime('%A').lower())
        lesson.save()