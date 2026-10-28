from django.test import TestCase
from django.urls import reverse

from .models import Choice, Course, Lesson, Question


class ExamFlowTests(TestCase):
    def setUp(self):
        self.course = Course.objects.create(name="Python Basics")
        Lesson.objects.create(course=self.course, title="Intro")
        self.q1 = Question.objects.create(course=self.course, question_text="2+2?", grade=1)
        self.right = Choice.objects.create(question=self.q1, choice_text="4", is_correct=True)
        Choice.objects.create(question=self.q1, choice_text="5", is_correct=False)
        self.q2 = Question.objects.create(course=self.course, question_text="Keyword for functions?", grade=1)
        self.right2 = Choice.objects.create(question=self.q2, choice_text="def", is_correct=True)
        Choice.objects.create(question=self.q2, choice_text="func", is_correct=False)

    def test_course_page_shows_name_and_lessons(self):
        resp = self.client.get(reverse("onlinecourse:course_details", args=[self.course.id]))
        self.assertContains(resp, "Python Basics")
        self.assertContains(resp, "Intro")

    def test_perfect_submission_passes(self):
        resp = self.client.post(
            reverse("onlinecourse:submit", args=[self.course.id]),
            {"choice": [self.right.id, self.right2.id]},
        )
        self.assertEqual(resp.status_code, 302)
        resp = self.client.get(resp["Location"])
        self.assertContains(resp, "Congratulations")
        self.assertContains(resp, "100%")

    def test_wrong_submission_fails(self):
        resp = self.client.post(
            reverse("onlinecourse:submit", args=[self.course.id]),
            {"choice": [self.right.id]},
        )
        resp = self.client.get(resp["Location"])
        self.assertNotContains(resp, "Congratulations")
        self.assertContains(resp, "50%")
