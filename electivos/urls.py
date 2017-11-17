from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

from . import views

app_name = 'electivos'

urlpatterns = [
    url(r'^courses$', views.CoursesView.as_view(), name="courses"),
    url(r'^courses/comments$', csrf_exempt(views.CommentView.as_view()), name="comment"),
    url(r'^courses/comments/like$', csrf_exempt(views.LikeView.as_view()), name="like"),
    url(r'^courses/comments/dislike$', csrf_exempt(views.DislikeView.as_view()), name="dislike")
]
