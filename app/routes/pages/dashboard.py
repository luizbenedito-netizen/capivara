from django.urls import path
from app.decorators import login_required
from app.views.dashboard import DashBoardView

urlpatterns = [
    path("", login_required(DashBoardView.as_view()), name="dashboard"),
]