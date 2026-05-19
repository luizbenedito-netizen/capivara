from django.http import JsonResponse
from django.views.decorators.http import require_POST

@require_POST
def context_date(request):

    month = request.POST.get('month')
    year = request.POST.get('year')

    try:
        month = int(month)
        year = int(year)

    except (TypeError, ValueError):
        return JsonResponse({
            'success': False,
            'error': 'Valores inválidos'
        }, status=400)

    if month < 1 or month > 12:
        return JsonResponse({
            'success': False,
            'error': 'Mês inválido'
        }, status=400)

    request.session['month'] = month
    request.session['year'] = year

    return JsonResponse({
        'success': True
    })

@require_POST
def context_theme(request):

    theme = request.POST.get('theme')

    if theme in ['light', 'dark']:

        request.session['theme'] = theme

        return JsonResponse({
            'success': True
        })

    return JsonResponse({
        'success': False
    }, status=400)