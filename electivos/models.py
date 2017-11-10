from django.db import models


class Course(models.Model):
    """
    Elective course of DCC.
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Comment(models.Model):
    """
    Comment for a Course.
    """
    course = models.ForeignKey(Course, related_name="comments")
    text = models.TextField()

    def __str__(self):
        return self.text[0: 50]
