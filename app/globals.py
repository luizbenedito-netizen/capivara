from datetime import datetime

MESES = [
    "Janeiro",
    "Fevereiro",
    "Março",
    "Abril",
    "Maio",
    "Junho",
    "Julho",
    "Agosto",
    "Setembro",
    "Outubro",
    "Novembro",
    "Dezembro",
]

def cache(request):

    now = datetime.now()

    month = int(request.session.get('month', now.month))
    year = int(request.session.get('year', now.year))

    return {
        'theme': request.session.get('theme', 'dark'),
        'month': month,
        'month_name': MESES[month - 1],
        'year': year,
    }