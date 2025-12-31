# pastes/urls.py
from django.urls import path
from .views import HealthzView, CreatePasteView, GetPasteAPIView, PasteHTMLView

urlpatterns = [
    path("api/healthz", HealthzView.as_view(), name="healthz"),
    path("api/pastes", CreatePasteView.as_view(), name="create_paste"),
    path("api/pastes/<uuid:id>", GetPasteAPIView.as_view(), name="get_paste"),
    path("p/<uuid:id>", PasteHTMLView.as_view(), name="paste_html"),
]
