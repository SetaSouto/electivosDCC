import json

from django.http import JsonResponse
from django.views import View
from django.views.generic import TemplateView

from electivos.models import Course, Comment


class Index(TemplateView):
    """
    Returns the index view, the homepage.
    """
    template_name = "electivos/index.html"


class CoursesView(View):
    """
    Return a json with all the data of the courses.
    """

    def get(self, request, *args, **kwargs):
        """
        Answer the get request.
        """
        courses = Course.objects.all()
        result = {}
        for course in courses:
            result[course.id] = {
                "name": course.name,
                "comments": [comment.text for comment in course.comments.all()]
            }
        return JsonResponse(result)


class CommentView(View):
    """
    Handles the post to create a comment.
    """

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            if not ("courseId" in data and "comment" in data):
                status = "Error, json must be {courseId: Number, comment: String}"
            else:
                status = "Error, course does not exists"
                if Course.objects.filter(id=data["courseId"]).exists():
                    Comment.objects.create(course=Course.objects.get(id=data["courseId"]), text=data["comment"])
                    status = "Success"
        except:
            status = "Error processing json"
        return JsonResponse({"status": status})
