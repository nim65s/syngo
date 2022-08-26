from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

app_name = "syngo"
urlpatterns = [
    path("", views.generate, name="generate"),
    path("<int:pk>", views.check, name="check"),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
