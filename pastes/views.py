from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import timedelta

from .models import Paste
from .utils import get_now


from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import connection

from django.db import transaction
from django.http import Http404

from django.shortcuts import render
from django.views import View


class HealthzView(APIView):
    """
    Health check endpoint.
    Confirms application can access persistence layer.
    """

    def get(self, request):
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1;")
            return Response({"ok": True}, status=200)
        except Exception:
            return Response({"ok": False}, status=500)


class CreatePasteView(APIView):
    """
    POST /api/pastes
    Creates a new paste.
    """

    def post(self, request):
        data = request.data

        content = data.get("content")
        ttl_seconds = data.get("ttl_seconds")
        max_views = data.get("max_views")

        # ---- Validation ----
        if not isinstance(content, str) or not content.strip():
            return Response(
                {"error": "content must be a non-empty string"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if ttl_seconds is not None:
            if not isinstance(ttl_seconds, int) or ttl_seconds < 1:
                return Response(
                    {"error": "ttl_seconds must be an integer >= 1"},
                    status=status.HTTP_400_BAD_REQUEST
                )

        if max_views is not None:
            if not isinstance(max_views, int) or max_views < 1:
                return Response(
                    {"error": "max_views must be an integer >= 1"},
                    status=status.HTTP_400_BAD_REQUEST
                )

        expires_at = None
        if ttl_seconds:
            expires_at = get_now(request) + timedelta(seconds=ttl_seconds)

        paste = Paste.objects.create(
            content=content,
            expires_at=expires_at,
            max_views=max_views
        )

        url = f"{request.scheme}://{request.get_host()}/p/{paste.id}"

        return Response(
            {
                "id": str(paste.id),
                "url": url
            },
            status=status.HTTP_201_CREATED
        )


class GetPasteAPIView(APIView):
    """
    GET /api/pastes/<id>
    Fetch a paste via API.
    Each successful fetch counts as a view.
    """

    def get(self, request, id):
        now = get_now(request)

        try:
            with transaction.atomic():
                paste = Paste.objects.select_for_update().get(id=id)

                # TTL check
                if paste.expires_at and now >= paste.expires_at:
                    return Response(
                        {"error": "Not found"},
                        status=status.HTTP_404_NOT_FOUND
                    )

                # View limit check
                if paste.max_views is not None and paste.views >= paste.max_views:
                    return Response(
                        {"error": "Not found"},
                        status=status.HTTP_404_NOT_FOUND
                    )

                paste.views += 1
                paste.save()

                remaining_views = None
                if paste.max_views is not None:
                    remaining_views = max(paste.max_views - paste.views, 0)

                return Response(
                    {
                        "content": paste.content,
                        "remaining_views": remaining_views,
                        "expires_at": paste.expires_at,
                    },
                    status=status.HTTP_200_OK
                )

        except Paste.DoesNotExist:
            return Response(
                {"error": "Not found"},
                status=status.HTTP_404_NOT_FOUND
            )



class PasteHTMLView(View):
    """
    GET /p/<id>
    HTML view for a paste.
    Counts as a view.
    """

    def get(self, request, id):
        now = get_now(request)

        try:
            with transaction.atomic():
                paste = Paste.objects.select_for_update().get(id=id)

                # TTL check
                if paste.expires_at and now >= paste.expires_at:
                    raise Http404()

                # View limit check
                if paste.max_views is not None and paste.views >= paste.max_views:
                    raise Http404()

                paste.views += 1
                paste.save()

            return render(request, "paste.html", {
                "content": paste.content
            })

        except Paste.DoesNotExist:
            raise Http404()
