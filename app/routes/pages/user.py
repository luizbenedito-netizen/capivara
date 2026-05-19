from django.urls import path
from app.decorators import login_required
from app.views.user import UserView, UserSettingsView

urlpatterns = [
    path("", login_required(UserView.as_view()), name="user"),
    path("settings/", login_required(UserSettingsView.as_view()), name="settings")
]