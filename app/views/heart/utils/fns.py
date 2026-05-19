from datetime import datetime
from django.db.models import Sum, Q
from django.db.models.functions import Coalesce
from decimal import Decimal
from app.models import CadUsuarios, Conta, ContaTipo, Receita, Despesa
from app.globals import cache as teste

# --- HELPER DE SESSÃO ---
def _obter_periodo_sessao(request):
    now = datetime.now()
    month = int(request.session.get('month', now.month))
    year = int(request.session.get('year', now.year))
    return month, year

# --- SELETORES DE DADOS (REUTILIZÁVEIS) ---
def buscar_dados_receita(user_id):

    totais = Conta.objects.filter(idusuario=user_id, status=1).aggregate(
        gloria_receitas=Coalesce(
            Sum('receita__valor', filter=Q(receita__status=1)), 
            Decimal('0.0')
        ),
        gloria_despesas=Coalesce(
            Sum('despesa__valor', filter=Q(despesa__status=1, despesa__data_removido__isnull=True)), 
            Decimal('0.0')
        )
    )

    saldo_geral_real = float(totais['gloria_receitas'] - totais['gloria_despesas'])
    
    return {
        'receita': saldo_geral_real  # Mantido a chave 'receita' para não quebrar seu front-end
    }

def buscar_dados_contas(user_id):
    ICONE_MAP = {
        1: "fa-wallet", 
        2: "fa-house", 
        3: "fa-basket-shopping", 
        4: "fa-plane", 
        5: "fa-health", 
        6: "fa-gamepad-modern"
    }

    contas = Conta.objects.filter(idusuario=user_id, status=1).annotate(
        total_receitas=Sum('receita__valor', filter=Q(receita__status=1)),
        total_despesas=Sum('despesa__valor', filter=Q(despesa__status=1, despesa__data_removido__isnull=True))
    )
    
    dados_finais = []
    for c in contas:
        receitas = c.total_receitas or 0
        despesas = c.total_despesas or 0
        saldo_real = float(receitas - despesas)
        
        dados_finais.append({
            'id': c.id,
            'nome_conta': c.nome_conta,
            'tipo_conta': c.tipo_conta.tipo_conta, # Garantindo que pegue a string do tipo_conta se necessário
            'icone': ICONE_MAP.get(c.icone, "fa-wallet"),
            'saldo_conta': saldo_real
        })
        
    return dados_finais

def buscar_listagem_receitas(request, user_id):
    month, year = _obter_periodo_sessao(request)
    receitas_query = Receita.objects.filter(
        idusuario=user_id, status=1, data_adicionada__month=month, data_adicionada__year=year
    ).order_by('-data_adicionada')
    
    total_somado = receitas_query.aggregate(total=Sum('valor'))['total'] or 0.00
    
    return {
        'lista': [
            {
                'id': r.id,
                'tipo_receita': r.tipo_receita,
                'valor': float(r.valor),
                'data_adicionada': r.data_adicionada.strftime('%d/%m/%Y')
            } for r in receitas_query
        ],
        'total_somado': float(total_somado)
    }

def buscar_listagem_despesas(request, user_id):
    month, year = _obter_periodo_sessao(request)
    despesas_query = Despesa.objects.filter(
        idusuario=user_id,
        data_removido__isnull=True,
        data_adicionado__month=month,
        data_adicionado__year=year
    ).order_by('status', 'data_vencimento')
    total_somado = despesas_query.aggregate(
        total_pendente=Sum('valor', filter=Q(status=0))
    )['total_pendente'] or 0.00
    
    return {
        'lista': [
            {
                'id': d.id,
                'nome': f"{d.nome} ({d.parcela_atual}/{d.total_parcelas})" if d.forma_pagamento == 'parcelado' else d.nome,
                'valor': float(d.valor),
                'vencimento': d.data_vencimento.strftime('%d/%m/%Y'),
                'status': d.status,
            } for d in despesas_query
        ],
        'total_somado': float(total_somado)
    }

def buscar_tipos_conta(user_id):
    tipos = ContaTipo.objects.filter(idusuario=user_id, status=1).order_by('tipo_conta')
    return [{'id': t.id, 'tipo_conta': t.tipo_conta} for t in tipos]


def sumario_financeiro(request, user_id):
    cacheValue = teste(request)
    mes_selecionado = cacheValue['month']
    ano_selecionado = cacheValue['year']
    totais_do_mes = Conta.objects.filter(idusuario=user_id, status=1).aggregate(
        total_receitas_mes=Coalesce(
            Sum('receita__valor', filter=Q(
                receita__status=1,
                receita__data_adicionada__month=mes_selecionado,
                receita__data_adicionada__year=ano_selecionado
            )), 
            Decimal('0.0')
        ),
        total_despesas_pagas_mes=Coalesce(
            Sum('despesa__valor', filter=Q(
                despesa__status=1, # Apenas pagas que impactaram o saldo
                despesa__data_removido__isnull=True,
                despesa__data_vencimento__month=mes_selecionado,
                despesa__data_vencimento__year=ano_selecionado
            )), 
            Decimal('0.0')
        )
    )
    receitas_total_real = float(totais_do_mes['total_receitas_mes'] - totais_do_mes['total_despesas_pagas_mes'])
    total_despesas_pendentes = Despesa.objects.filter(
        idusuario=user_id,
        status=0, # Apenas Pendentes
        data_removido__isnull=True,
        data_vencimento__month=mes_selecionado,
        data_vencimento__year=ano_selecionado
    ).aggregate(total=Sum('valor'))['total'] or 0.00
    
    return {
        'receitas_total': receitas_total_real,
        'despesas_total': float(total_despesas_pendentes),
        'mes_exibicao': mes_selecionado,
    }