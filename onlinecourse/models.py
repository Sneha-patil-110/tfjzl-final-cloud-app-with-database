from django.conf import settings
from django.db import models


class Instructor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    full_time = models.BooleanField(default=False)
    total_learners = models.IntegerField(default=0)

    def __str__(self):
        return self.user.get_username()


class Learner(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    occupation = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.get_username()


class Course(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    instructors = models.ManyToManyField(Instructor, blank=True)

    def __str__(self):
        return self.name


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons")
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)

    def __str__(self):
        return self.title


class Enrollment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="enrollments")
    date_enrolled = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.get_username()} enrolled in {self.course.name}"


class Question(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="questions")
    question_text = models.CharField(max_length=500)
    grade = models.IntegerField(default=1)

    def __str__(self):
        return self.question_text

    def is_get_score(self, selected_ids):
        """True only if the selected choices are exactly the correct ones."""
        correct_ids = set(self.choices.filter(is_correct=True).values_list("id", flat=True))
        return correct_ids == set(selected_ids)


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="choices")
    choice_text = models.CharField(max_length=100)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.choice_text


class Submission(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name="submissions", null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="submissions")
    choices = models.ManyToManyField(Choice)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Submission {self.id} for {self.enrollment or self.course}"
