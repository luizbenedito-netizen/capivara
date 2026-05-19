from django.contrib import admin
from django.urls import include, path
from app.views.errors.errors import error_404
from django.views.generic import RedirectView

urlpatterns = [
    path("", RedirectView.as_view(url="/home/", permanent=False)),
    path("admin/", admin.site.urls),
    path("api/", include("app.routes.api.__main__")),
    path("", include("app.routes.pages.__main__")),
]

handler404 = error_404