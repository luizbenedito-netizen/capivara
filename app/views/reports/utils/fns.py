from datetime import datetime, timedelta, time

from django.utils.timezone import make_aware
from app.models import Conta, Receita, Despesa


def relatorio_financeiro_view(user_id, request):

    data_inicio_str = request.GET.get('data_inicio')
    data_fim_str = request.GET.get('data_fim')
    conta_id = request.GET.get('conta')

    # DATA INÍCIO

    if not data_inicio_str:

        data_inicio = datetime.now() - timedelta(days=30)

        data_inicio_str = data_inicio.strftime('%Y-%m-%d')

    else:

        data_inicio = datetime.strptime(
            data_inicio_str,
            '%Y-%m-%d'
        )

    # DATA FIM

    if not data_fim_str:

        data_fim = datetime.now()

        data_fim_str = data_fim.strftime('%Y-%m-%d')

    else:

        data_fim = datetime.strptime(
            data_fim_str,
            '%Y-%m-%d'
        )

    # QUERY RECEITAS

    receitas_qs = Receita.objects.filter(
        idusuario=user_id,
        status=1,
        data_adicionada__date__range=[
            data_inicio.date(),
            data_fim.date()
        ]
    )

    # QUERY DESPESAS

    despesas_qs = Despesa.objects.filter(
        idusuario=user_id,
        data_removido__isnull=True,
        data_vencimento__range=[
            data_inicio.date(),
            data_fim.date()
        ]
    )

    # FILTRO CONTA

    if conta_id:

        receitas_qs = receitas_qs.filter(
            conta_id=conta_id
        )

        despesas_qs = despesas_qs.filter(
            conta_origem_id=conta_id
        )

    transacoes = []

    # RECEITAS

    for r in receitas_qs.select_related('conta'):

        transacoes.append({

            'data': r.data_adicionada,

            'tipo': 'Receita',

            'nome': r.tipo_receita,

            'conta': r.conta.nome_conta,

            'valor': r.valor,

            'classe_css': 'text-success'
        })

    # DESPESAS

    for d in despesas_qs.select_related('conta_origem'):

        data_vencimento_datetime = make_aware(
            datetime.combine(
                d.data_vencimento,
                time.min
            )
        )

        transacoes.append({

            'data': data_vencimento_datetime,

            'tipo': 'Despesa',

            'nome': d.nome,

            'conta': (
                d.conta_origem.nome_conta
                if d.conta_origem
                else 'Não informada'
            ),

            'valor': d.valor,

            'classe_css': 'text-danger'
        })

    # ORDENAÇÃO

    transacoes.sort(
        key=lambda x: x['data'],
        reverse=True
    )

    # CONTAS

    contas = Conta.objects.filter(
        idusuario=user_id,
        status=1
    ).order_by('nome_conta')

    return {

        'transacoes': transacoes,

        'contas': contas,

        'filtros': {

            'data_inicio': data_inicio_str,

            'data_fim': data_fim_str,

            'conta_id': int(conta_id)
            if conta_id else ''
        }
    }