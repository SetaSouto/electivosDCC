import json

from django.test import TestCase, Client
from django.urls import reverse

from electivos.models import Course, Comment


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        # create some data
        self.data = {"name": "Apps web", "comments": ["Buen curso", "entrete"]}
        c = Course.objects.create(name=self.data["name"])
        Comment.objects.create(course=c, text=self.data["comments"][0])
        Comment.objects.create(course=c, text=self.data["comments"][1])

    def test_get_courses(self):
        response = self.client.get(reverse("electivos:courses"))
        self.assertEqual(200, response.status_code)
        expected = {"1": self.data}
        self.assertEqual(expected, json.loads(response.content))

    def test_post_comment(self):
        url = reverse("electivos:comment")

        # MUST WORK
        data = {"courseId": 1, "comment": "Lo pasé super bien"}
        response = self.client.post(url, json.dumps(data), content_type="application/json")
        self.assertEqual(200, response.status_code)
        self.assertEqual({"status": "Success"}, json.loads(response.content))

        # MUST GIVE ERRORS
        for data in [{}, {"courseId": 2, "comment": "Buen curso"}]:
            response = self.client.post(url, json.dumps(data), content_type="application/json")
            self.assertEqual(200, response.status_code)
            self.assertNotEqual({"status": "Success"}, json.loads(response.content))
