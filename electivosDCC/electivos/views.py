from django.http import JsonResponse
from django.views import View
from django.views.generic import TemplateView

from electivos.models import Course


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
