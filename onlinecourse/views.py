from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .models import Choice, Course, Enrollment, Submission

PASS_PERCENT = 70


def course_details(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    return render(request, "onlinecourse/course_details_bootstrap.html", {"course": course})


@require_POST
def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    user = request.user if request.user.is_authenticated else None
    enrollment = None
    if user is not None:
        enrollment, _ = Enrollment.objects.get_or_create(user=user, course=course)
    submission = Submission.objects.create(user=user, course=course, enrollment=enrollment)
    selected_ids = request.POST.getlist("choice")
    submission.choices.set(Choice.objects.filter(pk__in=selected_ids, question__course=course))
    return redirect("onlinecourse:show_exam_result", course_id=course.id, submission_id=submission.id)


def show_exam_result(request, course_id, submission_id):
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(Submission, pk=submission_id, course=course)
    selected_ids = set(submission.choices.values_list("id", flat=True))

    results = []
    total_grade = 0
    earned_grade = 0
    for question in course.questions.prefetch_related("choices"):
        chosen = [c for c in question.choices.all() if c.id in selected_ids]
        correct = question.is_get_score([c.id for c in chosen])
        total_grade += question.grade
        if correct:
            earned_grade += question.grade
        results.append({"question": question, "chosen": chosen, "correct": correct})

    score_percent = round(100 * earned_grade / total_grade) if total_grade else 0
    context = {
        "course": course,
        "submission": submission,
        "results": results,
        "earned_grade": earned_grade,
        "total_grade": total_grade,
        "score_percent": score_percent,
        "total_score": earned_grade,
        "possible_score": total_grade,
        "grade": score_percent,
        "selected_ids": sorted(selected_ids),
        "passed": score_percent >= PASS_PERCENT,
        "pass_mark": PASS_PERCENT,
    }
    return render(request, "onlinecourse/exam_result_bootstrap.html", context)
