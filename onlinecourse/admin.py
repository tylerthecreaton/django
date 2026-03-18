from django.contrib import admin

from .models import (
    Learner,
    Instructor,
    Course,
    Enrollment,
    Lesson,
    Question,
    Choice,
    Submission,
)


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("question_text", "lesson", "grade")
    inlines = [ChoiceInline]


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("title", "course", "order")
    list_filter = ("course",)
    inlines = [QuestionInline]


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name", "description")
    filter_horizontal = ("instructors",)
    inlines = [LessonInline]


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ("learner", "course", "enrolled_at")
    list_filter = ("course", "enrolled_at")
    search_fields = ("learner__user__username", "course__name")
    ordering = ("-enrolled_at",)


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ("enrollment", "submitted_at")


@admin.register(Learner)
class LearnerAdmin(admin.ModelAdmin):
    list_display = ("user", "occupation")


@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ("user", "full_time")
