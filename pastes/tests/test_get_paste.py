from django.test import TestCase
from django.urls import reverse
from pastes.models import Paste
from django.utils import timezone
import datetime

class GetPasteTest(TestCase):

    def test_fetch_existing_paste(self):
        paste = Paste.objects.create(content="Fetch Test")
        url = reverse("get_paste", args=[paste.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["content"], "Fetch Test")

    def test_fetch_missing_paste_returns_404(self):
        url = reverse("get_paste", args=["00000000-0000-0000-0000-000000000000"])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_max_views_limit(self):
        paste = Paste.objects.create(content="MaxViews", max_views=1)
        url = reverse("get_paste", args=[paste.id])
        r1 = self.client.get(url)
        self.assertEqual(r1.status_code, 200)
        r2 = self.client.get(url)
        self.assertEqual(r2.status_code, 404)

    def test_ttl_expiry(self):
        now = timezone.now()
        paste = Paste.objects.create(content="TTL Test",
                                     expires_at=now + datetime.timedelta(seconds=1))
        url = reverse("get_paste", args=[paste.id])
        expired_ms = int((now + datetime.timedelta(seconds=2)).timestamp() * 1000)
        r = self.client.get(url, HTTP_X_TEST_NOW_MS=str(expired_ms))
        self.assertEqual(r.status_code, 404)
