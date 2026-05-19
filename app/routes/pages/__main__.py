from django.urls import include, path

urlpatterns = [
    # Módulos do Página
    path("login/", include("app.routes.pages.login")),
    path("register/", include("app.routes.pages.register")),
    path("home/", include("app.routes.pages.heart")),
    path("dashboard/", include("app.routes.pages.dashboard")),
    path("reports/", include("app.routes.pages.reports")),
    path("calc/", include("app.routes.pages.calc")),
    path("user/", include("app.routes.pages.user")),
]