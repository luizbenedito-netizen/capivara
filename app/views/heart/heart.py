from django.shortcuts import render, redirect
from django.views import View
from app.views.heart.utils import fns
from app.utils.fns import get_greeting

class HeartView(View):
    def get(self, request, user_id, *args, **kwargs):

        return render(request, 'pages/home/home.html', {
            'active_page': 'home',
            'greeting': get_greeting(),
            'sumario_financeiro': fns.sumario_financeiro(request, user_id),
            'financeiro': fns.buscar_dados_receita(user_id),
            'contas': fns.buscar_dados_contas(user_id),
            'receitas_detalhado': fns.buscar_listagem_receitas(request, user_id),
            'despesas_detalhado': fns.buscar_listagem_despesas(request, user_id),
            'tipos_conta': fns.buscar_tipos_conta(user_id)
        })