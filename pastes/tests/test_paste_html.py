from django.test import TestCase
from django.urls import reverse
from pastes.models import Paste
from django.utils import timezone
import datetime

class PasteHTMLTest(TestCase):

    def test_html_renders_content_safely(self):
        paste = Paste.objects.create(content="<script>alert('xss')</script>")
        url = reverse("paste_html", args=[paste.id])
        r = self.client.get(url)
        self.assertEqual(r.status_code, 200)
        html = r.content.decode()
        self.assertIn("&lt;script&gt;alert(&#x27;xss&#x27;)&lt;/script&gt;", html)

    def test_html_max_views(self):
        paste = Paste.objects.create(content="HTML MaxViews", max_views=1)
        url = reverse("paste_html", args=[paste.id])
        r1 = self.client.get(url)
        self.assertEqual(r1.status_code, 200)
        r2 = self.client.get(url)
        self.assertEqual(r2.status_code, 404)

    def test_html_ttl_expiry(self):
        now = timezone.now()
        paste = Paste.objects.create(content="HTML TTL",
                                     expires_at=now + datetime.timedelta(seconds=1))
        url = reverse("paste_html", args=[paste.id])
        expired_ms = int((now + datetime.timedelta(seconds=2)).timestamp() * 1000)
        r = self.client.get(url, HTTP_X_TEST_NOW_MS=str(expired_ms))
        self.assertEqual(r.status_code, 404)

    def test_html_missing_paste(self):
        url = reverse("paste_html", args=["00000000-0000-0000-0000-000000000000"])
        r = self.client.get(url)
        self.assertEqual(r.status_code, 404)
