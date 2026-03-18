from django.contrib.auth.models import User
from django.db import models


class Learner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    occupation = models.CharField(max_length=120, blank=True)

    def __str__(self):
        return self.user.username


class Instructor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_time = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username


class Course(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    instructors = models.ManyToManyField(Instructor, related_name="courses", blank=True)

    def __str__(self):
        return self.name


class Enrollment(models.Model):
    learner = models.ForeignKey(Learner, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("learner", "course")

    def __str__(self):
        return f"{self.learner} - {self.course}"


class Lesson(models.Model):
    course = models.ForeignKey(Course, related_name="lessons", on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.title


class Question(models.Model):
    lesson = models.ForeignKey(
        Lesson, related_name="questions", on_delete=models.CASCADE
    )
    question_text = models.CharField(max_length=500)
    grade = models.PositiveIntegerField(default=1)

    def is_get_score(self, selected_choice_ids):
        correct_choice_ids = set(
            self.choices.filter(is_correct=True).values_list("id", flat=True)
        )
        selected_choice_ids = set(selected_choice_ids)
        question_choice_ids = set(self.choices.values_list("id", flat=True))
        selected_for_question = selected_choice_ids.intersection(question_choice_ids)
        return bool(correct_choice_ids) and selected_for_question == correct_choice_ids

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(
        Question, related_name="choices", on_delete=models.CASCADE
    )
    choice_text = models.CharField(max_length=300)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.choice_text


class Submission(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
    choices = models.ManyToManyField(Choice)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def score(self):
        total = 0
        earned = 0

        questions = Question.objects.filter(
            lesson__course=self.enrollment.course
        ).prefetch_related("choices")
        selected_ids = set(self.choices.values_list("id", flat=True))

        for question in questions:
            total += question.grade
            correct_ids = set(
                question.choices.filter(is_correct=True).values_list("id", flat=True)
            )
            selected_for_question = selected_ids.intersection(
                set(question.choices.values_list("id", flat=True))
            )
            if correct_ids and selected_for_question == correct_ids:
                earned += question.grade

        return earned, total
