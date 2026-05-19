from django.urls import path
from app.views.login import RegisterView

urlpatterns = [
    path("", RegisterView.as_view(), name="register")
]