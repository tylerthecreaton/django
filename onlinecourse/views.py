from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth.models import User

from .models import Choice, Course, Enrollment, Learner, Submission


@require_GET
def course_details(request, course_id):
    course = get_object_or_404(Course.objects.prefetch_related("lessons"), pk=course_id)
    return render(
        request, "onlinecourse/course_details_bootstrap.html", {"course": course}
    )


@require_POST
def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)

    default_user, _ = User.objects.get_or_create(
        username="demo_learner",
        defaults={"email": "demo@example.com"},
    )
    learner, _ = Learner.objects.get_or_create(user=default_user)

    enrollment, _ = Enrollment.objects.get_or_create(
        course=course,
        learner=learner,
    )

    selected_choice_ids = []
    for key, value in request.POST.items():
        if key.startswith("choice_"):
            selected_choice_ids.append(value)

    submission = Submission.objects.create(enrollment=enrollment)
    if selected_choice_ids:
        choices = Choice.objects.filter(id__in=selected_choice_ids)
        submission.choices.set(choices)

    return redirect(
        "onlinecourse:show_exam_result",
        course_id=course.id,
        submission_id=submission.id,
    )


@require_GET
def show_exam_result(request, course_id, submission_id):
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(
        Submission, pk=submission_id, enrollment__course=course
    )
    earned, total = submission.score()

    passed = False
    if total > 0:
        passed = (earned / total) >= 0.6

    context = {
        "course": course,
        "submission": submission,
        "earned": earned,
        "total": total,
        "passed": passed,
    }
    return render(request, "onlinecourse/exam_result_bootstrap.html", context)
