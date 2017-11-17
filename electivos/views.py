import json

from django.http import JsonResponse
from django.http import HttpResponse
from django.views import View
from django.views.generic import TemplateView
from django.template import loader

from electivos.models import Course, Comment


class Index(TemplateView):
    """
    Returns the index view, the homepage.
    """
    def get(self, request, *args, **kwargs):
        return HttpResponse(loader.get_template('build/index.html').render())


class CoursesView(View):
    """
    Return a json with all the data of the courses.
    """

    def get(self, request, *args, **kwargs):
        """
        Answer the get request.
        """
        courses = Course.objects.all()
        electivos = []
        for course in courses:
            electivos.append({
                "name": course.name,
                "id": course.id,
                "comments": [{"id": comment.id,
                              "txt": comment.text,
                              "votes": {
                                  "up": comment.likes,
                                  "down": comment.dislikes,
                              }} for comment in course.comments.all()]
            })
        return JsonResponse({"electivos": electivos})


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


class LikeView(View):
    """
    Handles a like post.
    """

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            status = "Error, comment does not exists"
            if "id" in data and Comment.objects.filter(id=data["id"]).exists():
                c = Comment.objects.get(id=data["id"])
                c.likes += 1
                c.save()
                status = "Success"
        except:
            status = "Error processing json"
        return JsonResponse({"status": status})
