from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from app.decorators import api_login_required
from django.db.models import Sum
from datetime import datetime
from app.globals import cache as teste
from app.models import Despesa, Receita

@api_login_required
@require_http_methods(["GET"])
def dashboard_despesas_categorias(request, user_id):
    try:
        cacheValue = teste(request)
        month = cacheValue['month']
        year = cacheValue['year']
        despesas = (
            Despesa.objects
            .filter(
                idusuario=user_id,
                data_removido__isnull=True,
                data_vencimento__month=month,
                data_vencimento__year=year
            )
            .values('tipo')
            .annotate(total=Sum('valor'))
            .order_by('-total')
        )
        labels = []
        valores = []
        for item in despesas:
            labels.append(item['tipo'])
            valores.append(float(item['total']))

        return JsonResponse({
            'success': True,
            'labels': labels,
            'valores': valores
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

@api_login_required
@require_http_methods(["GET"])
def dashboard_receitas_despesas(request, user_id):
    try:
        cacheValue = teste(request)
        month = cacheValue['month']
        year = cacheValue['year']
        total_receitas = (
            Receita.objects
            .filter(
                idusuario=user_id,
                data_remocao__isnull=True,
                data_adicionada__month=month,
                data_adicionada__year=year
            )
            .aggregate(total=Sum('valor'))
        )['total'] or 0
        total_despesas = (
            Despesa.objects
            .filter(
                idusuario=user_id,
                data_removido__isnull=True,
                data_vencimento__month=month,
                data_vencimento__year=year
            )
            .aggregate(total=Sum('valor'))
        )['total'] or 0
        return JsonResponse({
            'success': True,

            'labels': [
                'Receitas',
                'Despesas'
            ],

            'valores': [
                float(total_receitas),
                float(total_despesas)
            ]
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)