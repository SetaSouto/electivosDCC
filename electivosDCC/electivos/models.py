from django.db import models


class Course(models.Model):
    """
    Elective course of DCC.
    """
    name = models.CharField(max_length=100)


class Comment(models.Model):
    """
    Comment for a Course.
    """
    course = models.ForeignKey(Course, related_name="comments")
    text = models.TextField()
