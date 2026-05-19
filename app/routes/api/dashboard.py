from django.urls import path
from app.views.dashboard.api import dash

urlpatterns = [
    path('despesas-categorias/', dash.dashboard_despesas_categorias, name='dashboard_despesas_categorias'),
    path('receitas-despesas/', dash.dashboard_receitas_despesas, name='dashboard_receitas_despesas')
]