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
    Receives a JSON as {"id": id of the course, "comment": String}
    """

    def post(self, request, *args, **kwargs):
        status_code = 400
        createdComment = None
        try:
            data = json.loads(request.body)
            if not ("id" in data and "comment" in data):
                status = "Error, json must be {id: Number, comment: String}"
            else:
                status = "Error, course does not exists"
                if Course.objects.filter(id=data["id"]).exists():
                    createdComment = Comment.objects.create(course=Course.objects.get(id=data["id"]),
                                                            text=data["comment"])
                    status = "Success"
                    status_code = 200
        except:
            status = "Error processing json"
        response = {"status": status}
        if (createdComment): response["id"] = createdComment.id
        return JsonResponse(response, status=status_code)


class BaseLikesView(View):
    """
    Base class to handle the request to like/dislike a comment.
    """

    def handle_action(self):
        """
        Handles the action, the comment object is in self.comment.
        """
        raise NotImplementedError()

    def post(self, request, *args, **kwargs):
        status_code = 400
        try:
            data = json.loads(request.body)
            status = "Error, comment does not exists"
            if "id" in data and Comment.objects.filter(id=data["id"]).exists():
                self.comment = Comment.objects.get(id=data["id"])
                self.handle_action()
                self.comment.save()
                status = "Success"
                status_code = 200
        except:
            status = "Error processing json"
        return JsonResponse({"status": status}, status=status_code)


class LikeView(BaseLikesView):
    """
    Handles a like post.
    """

    def handle_action(self):
        self.comment.likes += 1


class DislikeView(BaseLikesView):
    """
    Handles the dislike post.
    """

    def handle_action(self):
        self.comment.dislikes += 1
