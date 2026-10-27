# CourseraAssn: Online Course app with mock exam

Django app (`onlinecourse`) with course lessons, exam questions and choices, a submission view, and a result view that scores the attempt.

## Run

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Create a course, lessons and questions in `/admin/`, then open `/course/<id>/`.

## Exam routes

- `course/<id>/` course detail page (lessons + exam)
- `course/<id>/submit/` POST handler that stores the submission
- `course/<id>/submission/<id>/result/` scores the submission; 70% passes

## Tests

```bash
python manage.py test onlinecourse
```
