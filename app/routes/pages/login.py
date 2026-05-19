from django.urls import path
from app.views.login import LoginView, EsqueciSenhaView, ResetarSenhaView

urlpatterns = [
    path("", LoginView.as_view(), name="login"),
    path("logout/", LoginView.logout, name="logout"),
    path("esquecisenha/", EsqueciSenhaView.as_view(), name="esqueci"),
    path("esquecisenha/<path:token>/", ResetarSenhaView.as_view(), name="recover"),
]