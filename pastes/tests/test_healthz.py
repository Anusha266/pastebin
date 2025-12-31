from django.test import TestCase
from django.urls import reverse
import json

class HealthzTest(TestCase):
    def test_healthz_returns_ok(self):
        url = reverse("healthz")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"ok": True})
