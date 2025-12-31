from datetime import datetime, timezone
from django.conf import settings


def get_now(request):
    """
    Returns current time.
    In TEST_MODE, uses x-test-now-ms header if present.
    """
    if getattr(settings, "TEST_MODE", False):
        test_now = request.headers.get("x-test-now-ms")
        if test_now:
            return datetime.fromtimestamp(int(test_now) / 1000, tz=timezone.utc)

    return datetime.now(tz=timezone.utc)
