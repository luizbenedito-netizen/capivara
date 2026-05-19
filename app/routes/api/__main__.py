from django.urls import include, path

urlpatterns = [
    # Módulos do API
    path("login/", include("app.routes.api.login")),
    path("heart/", include("app.routes.api.heart")),
    path("context/", include("app.routes.api.context")),
    path("dashboard/", include("app.routes.api.dashboard")),
]