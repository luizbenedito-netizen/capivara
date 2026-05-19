from django.urls import path
from app.views.context import context_theme, context_date

urlpatterns = [
    path('theme/', context_theme, name='theme'),
    path('date/', context_date, name='theme'),
]