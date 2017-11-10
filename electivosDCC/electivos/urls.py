from django.conf.urls import url

from . import views

app_name = 'electivos'

urlpatterns = [
    url(r'^courses', views.CoursesView.as_view(), name="courses")
]
