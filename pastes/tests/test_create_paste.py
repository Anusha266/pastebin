from django.test import TestCase
from django.urls import reverse
import json

class CreatePasteTest(TestCase):

    def test_create_valid_paste(self):
        url = reverse("create_paste")
        data = {"content": "Valid paste"}
        response = self.client.post(url, json.dumps(data), content_type="application/json")
        self.assertIn(response.status_code, [200, 201])
        res_json = response.json()
        self.assertIn("id", res_json)
        self.assertIn("url", res_json)

    def test_create_with_ttl(self):
        url = reverse("create_paste")
        data = {"content": "TTL paste", "ttl_seconds": 10}
        response = self.client.post(url, json.dumps(data), content_type="application/json")
        self.assertIn(response.status_code, [200, 201])
        self.assertTrue(response.json()["id"])

    def test_create_with_max_views(self):
        url = reverse("create_paste")
        data = {"content": "MaxViews paste", "max_views": 2}
        response = self.client.post(url, json.dumps(data), content_type="application/json")
        self.assertIn(response.status_code, [200, 201])
        self.assertTrue(response.json()["id"])

    def test_create_invalid_empty_content(self):
        url = reverse("create_paste")
        data = {"content": ""}
        response = self.client.post(url, json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_create_invalid_ttl_or_views(self):
        url = reverse("create_paste")
        data = {"content": "x", "ttl_seconds": 0}
        response = self.client.post(url, json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 400)

        data = {"content": "x", "max_views": 0}
        response = self.client.post(url, json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 400)
