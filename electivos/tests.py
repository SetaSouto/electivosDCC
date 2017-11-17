import json

from django.test import TestCase, Client
from django.urls import reverse

from electivos.models import Course, Comment


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        # create some data
        self.data = {"name": "Apps web", "comments": ["Buen curso", "entrete"]}
        self.course = Course.objects.create(name=self.data["name"])
        Comment.objects.create(course=self.course, text=self.data["comments"][0])
        Comment.objects.create(course=self.course, text=self.data["comments"][1])

    def test_get_courses(self):
        expected = {"electivos": [{
            "name": self.course.name,
            "id": self.course.id,
            "comments": [{"id": comment.id,
                          "txt": comment.text,
                          "votes": {
                              "up": comment.likes,
                              "down": comment.dislikes
                          }} for comment in self.course.comments.all()]
        }]}

        response = self.client.get(reverse("electivos:courses"))
        self.assertEqual(200, response.status_code)
        self.assertEqual(expected, json.loads(response.content))

    def test_post_comment(self):
        url = reverse("electivos:comment")

        # MUST WORK
        data = {"id": 1, "comment": "Lo pasé super bien"}
        response = self.client.post(url, json.dumps(data), content_type="application/json")
        self.assertEqual(200, response.status_code)
        self.assertEqual({"status": "Success", "id": Comment.objects.get(text=data["comment"]).id},
                         json.loads(response.content))

        # MUST GIVE ERRORS
        for data in [{}, {"id": 2, "comment": "Buen curso"}]:
            response = self.client.post(url, json.dumps(data), content_type="application/json")
            self.assertEqual(400, response.status_code)
            self.assertNotEqual({"status": "Success"}, json.loads(response.content))

    def test_likes_dislikes(self):
        url_like = reverse("electivos:like")
        url_dislike = reverse("electivos:dislike")

        # WRONG ID
        data = {"id": "not an id"}

        response = self.client.post(url_like, json.dumps(data), content_type="application/json")

        self.assertEqual(400, response.status_code)

        # CREATE COMMENT

        comment = Comment.objects.create(course=self.course, text="Random comment")

        data = {"id": comment.id}

        # LIKE
        response = self.client.post(url_like, json.dumps(data), content_type="application/json")

        self.assertEqual(200, response.status_code)
        self.assertEqual(1, Comment.objects.get(id=comment.id).likes)
        self.assertEqual({"status": "Success"}, json.loads(response.content))

        # DISLIKE
        response = self.client.post(url_dislike, json.dumps(data), content_type="application/json")

        self.assertEqual(200, response.status_code)
        self.assertEqual(1, Comment.objects.get(id=comment.id).dislikes)
        self.assertEqual({"status": "Success"}, json.loads(response.content))
