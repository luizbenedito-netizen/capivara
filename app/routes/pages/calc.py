from django.urls import path
from app.decorators import login_required
from app.views.calc import CalcView

urlpatterns = [
    path("", login_required(CalcView.as_view()), name="calc"),
]