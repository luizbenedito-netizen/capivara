from django.views import View
from django.shortcuts import render, redirect
from app.utils.fns import get_greeting
from app.views.heart.utils import fns as fns_home
from app.views.reports.utils import fns

class ReportsView(View):
    def get(self, request, user_id, *args, **kwargs):

        dados_template = {
            'active_page': 'reports',
            'greeting': get_greeting(),
            'sumario_financeiro': fns_home.sumario_financeiro(request, user_id),
        }
        dados_relatorio = fns.relatorio_financeiro_view(user_id, request)
        dados_template.update(dados_relatorio)
        return render(request, 'pages/reports/reports.html', dados_template)

    def post(self, request, user_id, *args, **kwargs):
        return True