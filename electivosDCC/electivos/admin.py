from django.contrib import admin

from electivos.models import Course, Comment


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    pass


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass
