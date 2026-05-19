from django.views import View
from django.shortcuts import render, redirect
from app.utils.fns import get_greeting
from app.views.heart.utils import fns

class CalcView(View):

    def get(self, request, user_id, *args, **kwargs):
        return render(request, 'pages/calc/calc.html' , {
            'active_page': 'calc',
            'greeting': get_greeting(),
            'sumario_financeiro': fns.sumario_financeiro(request, user_id)
        })

    def post(self, request, *args, **kwargs):
        return True