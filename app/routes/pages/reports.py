from django.urls import path
from app.decorators import login_required
from app.views.reports import ReportsView

urlpatterns = [
    path("", login_required(ReportsView.as_view()), name="reports"),
]