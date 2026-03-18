import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "onlinecourse_project.settings")

import django

django.setup()

from django.contrib.auth.models import User

from onlinecourse.models import Choice, Course, Lesson, Question


if not User.objects.filter(username="admin").exists():
    User.objects.create_superuser("admin", "admin@example.com", "admin1234")

course, _ = Course.objects.get_or_create(
    name="Python for Beginners",
    defaults={"description": "Sample course for final project"},
)

lesson1, _ = Lesson.objects.get_or_create(
    course=course,
    order=1,
    defaults={"title": "Basics", "content": "Introduction to Python"},
)

question1, _ = Question.objects.get_or_create(
    lesson=lesson1,
    question_text="Python is dynamically typed?",
    defaults={"grade": 1},
)

Choice.objects.get_or_create(
    question=question1,
    choice_text="True",
    defaults={"is_correct": True},
)
Choice.objects.get_or_create(
    question=question1,
    choice_text="False",
    defaults={"is_correct": False},
)

lesson2, _ = Lesson.objects.get_or_create(
    course=course,
    order=2,
    defaults={"title": "Web with Django", "content": "Django fundamentals"},
)

question2, _ = Question.objects.get_or_create(
    lesson=lesson2,
    question_text="Django follows MTV pattern?",
    defaults={"grade": 1},
)

Choice.objects.get_or_create(
    question=question2,
    choice_text="Yes",
    defaults={"is_correct": True},
)
Choice.objects.get_or_create(
    question=question2,
    choice_text="No",
    defaults={"is_correct": False},
)

print(f"Seed complete. Course ID: {course.id}")
