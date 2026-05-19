from django.views.decorators.http import require_http_methods
from datetime import datetime
from django.http import JsonResponse
from app.models import Receita, Despesa, Conta
from app.decorators import api_login_required
from django.db.models import Sum

@api_login_required
def buscar_tipos_conta(request, user_id):
    contas = Conta.objects.filter(idusuario=user_id, status=1).order_by('nome_conta')
    dados_contas = [{'id': c.id, 'nome_conta': c.nome_conta} for c in contas]
    return JsonResponse(dados_contas, safe=False)

@api_login_required 
@require_http_methods(["POST"])
def api_criar_receita(request, user_id):
    try:
        valor = request.POST.get('valor')
        conta_id = request.POST.get('conta_id')
        tipo_receita = request.POST.get('tipo_receita', 'Receita Geral')

        if not valor or not conta_id:
            return JsonResponse({'error': 'Valor e Conta são obrigatórios.'}, status=400)

        # Valida se a conta existe e pertence ao usuário
        conta = Conta.objects.get(id=conta_id, idusuario=user_id)

        nova_receita = Receita.objects.create(
            idusuario=user_id,
            conta=conta,
            tipo_receita=tipo_receita,
            valor=valor,
            status=1  # Ativo/Padrão
        )

        return JsonResponse({'success': True, 'id': nova_receita.id})

    except Conta.DoesNotExist:
        return JsonResponse({'error': 'A carteira informada não existe ou não pertence a você.'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@api_login_required 
@require_http_methods(["POST"]) 
def api_criar_despesa(request, user_id): 
    try: 
        nome = request.POST.get('nome') 
        tipo = request.POST.get('tipo', 'Geral') 
        subgrupo = request.POST.get('subgrupo') 
        valor = request.POST.get('valor') 
        data_vencimento = request.POST.get('data_vencimento') 
        descricao = request.POST.get('descricao') 
        conta_id = request.POST.get('conta_id') 

        # 1. REMOVIDO conta_id
        if not all([nome, valor, data_vencimento]): 
            return JsonResponse({'error': 'Campos obrigatórios ausentes.'}, status=400) 

        # 2. Trata 'null'
        conta_origem = None
        if conta_id and conta_id not in ['null', '', 'None']:
            try:
                # Só busca no banco se realmente veio um ID válido
                conta_origem = Conta.objects.get(id=conta_id, idusuario=user_id)
            except Conta.DoesNotExist:
                return JsonResponse({'error': 'A conta de origem não foi encontrada ou não pertence a você.'}, status=404)

        # 3. Cria a despesa salvando a conta
        nova_despesa = Despesa.objects.create( 
            idusuario=user_id, 
            conta_origem=conta_origem,
            nome=nome, 
            tipo=tipo, 
            subgrupo=subgrupo if subgrupo else None, 
            valor=valor, 
            data_vencimento=data_vencimento, 
            descricao=descricao if descricao else None, 
            status=0, 
            forma_pagamento='avista', 
            parcela_atual=1, 
            total_parcelas=1 
        ) 
        
        return JsonResponse({'success': True, 'id': nova_despesa.id}) 

    except Exception as e: 
        return JsonResponse({'error': str(e)}, status=500)


@api_login_required
@require_http_methods(["POST"])
def api_pagar_despesa(request, user_id, despesa_id):
    try:
        conta_id = request.POST.get('conta_id')
        if not conta_id:
            return JsonResponse({'error': 'ID da conta destino é obrigatório.'}, status=400)
        despesa = Despesa.objects.get(id=despesa_id, idusuario=user_id)
        conta = Conta.objects.get(id=conta_id, idusuario=user_id)
        saldo_conta = Receita.objects.filter(
            conta=conta, 
            idusuario=user_id, 
            status=1
        ).aggregate(Sum('valor'))['valor__sum'] or 0
        if saldo_conta < despesa.valor:
            return JsonResponse({'error': f'Saldo insuficiente. Saldo atual: R$ {saldo_conta:.2f}'}, status=400)
        despesa.status = 1  # Pago
        despesa.conta_origem = conta
        despesa.save()
        return JsonResponse({'success': True, 'message': 'Despesa paga com sucesso!'})
    except Despesa.DoesNotExist:
        return JsonResponse({'error': 'Despesa não encontrada.'}, status=404)
    except Conta.DoesNotExist:
        return JsonResponse({'error': 'Conta informada não existe.'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@api_login_required
@require_http_methods(["POST"])
def api_remover_despesa(request, user_id, despesa_id):
    try:
        despesa = Despesa.objects.get(id=despesa_id, idusuario=user_id)
        despesa.data_removido = datetime.now()
        despesa.save()
        return JsonResponse({'success': True, 'message': 'Despesa removida.'})
    except Despesa.DoesNotExist:
        return JsonResponse({'error': 'Despesa não encontrada.'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@api_login_required
@require_http_methods(["POST"])
def api_remover_receita(request, user_id, receita_id):
    try:
        receita = Receita.objects.get(id=receita_id, idusuario=user_id)
        receita.status = 0  # Desativado/Removido
        receita.save()
        return JsonResponse({'success': True, 'message': 'Receita removida.'})
    except Receita.DoesNotExist:
        return JsonResponse({'error': 'Receita não encontrada.'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)