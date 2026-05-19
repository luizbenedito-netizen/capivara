from django.urls import path
from app.decorators import login_required
from app.views.heart import heart

urlpatterns = [
    path("", login_required(heart.HeartView.as_view()), name="heart"),
]