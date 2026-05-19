import json
from datetime import datetime
from functools import wraps
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from app.decorators import api_login_required
from app.models import Conta, ContaTipo
from app.views.heart.utils import fns

# --- ENDPOINTS DE LEITURA (GET) ---
@api_login_required
def api_obter_receita(request, user_id):
    return JsonResponse(fns.buscar_dados_receita(user_id))

@api_login_required
def api_listar_contas(request, user_id):
    return JsonResponse({'contas': fns.buscar_dados_contas(user_id)}, safe=False)

@api_login_required
def api_listar_tipos_conta(request, user_id):
    return JsonResponse(fns.buscar_tipos_conta(user_id), safe=False)

@api_login_required
@require_http_methods(["GET"])
def api_detalhes_conta(request, user_id, id):
    try:
        conta = Conta.objects.get(id=id, idusuario=user_id, status=1)
        return JsonResponse({
            'success': True,
            'id': conta.id,
            'nome_conta': conta.nome_conta,
            'tipo_conta_id': conta.tipo_conta.id,
            'icone': conta.icone
        })
    except Conta.DoesNotExist:
        return JsonResponse({'error': 'Conta não encontrada'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# --- ENDPOINTS DE MANIPULAÇÃO (POST / DELETE) ---
@api_login_required
@require_http_methods(["POST"])
def api_criar_tipo_conta(request, user_id):
    tipo_conta = request.POST.get('tipo_conta', '').strip()
    if not tipo_conta:
        return JsonResponse({'error': 'Tipo de conta inválido'}, status=400)

    if ContaTipo.objects.filter(idusuario=user_id, tipo_conta__iexact=tipo_conta, status=1).exists():
        return JsonResponse({'error': 'Esse tipo de conta já existe'}, status=400)

    novo_tipo = ContaTipo.objects.create(idusuario=user_id, tipo_conta=tipo_conta, status=1)
    return JsonResponse({'success': True, 'id': novo_tipo.id, 'tipo_conta': novo_tipo.tipo_conta})

@api_login_required
@require_http_methods(["DELETE"])
def api_excluir_tipo_conta(request, user_id, id):
    try:
        tipo_conta = ContaTipo.objects.get(id=id, idusuario=user_id, status=1)
        tipo_conta.status = 0
        tipo_conta.save()
        return JsonResponse({'success': True})
    except ContaTipo.DoesNotExist:
        return JsonResponse({'error': 'Registro não encontrado'}, status=404)

@api_login_required
@require_http_methods(["POST"])
def api_criar_conta(request, user_id):
    try:
        data = json.loads(request.body)
        tipo_conta_id = data.get('tipo_conta')
        nome_conta = data.get('nome_conta', '').strip()
        icone = data.get('icone', '')

        if not tipo_conta_id or not nome_conta:
            return JsonResponse({'error': 'Dados inválidos'}, status=400)

        tipo_conta = ContaTipo.objects.get(id=tipo_conta_id, idusuario=user_id, status=1)
        conta = Conta.objects.create(idusuario=user_id, tipo_conta=tipo_conta, nome_conta=nome_conta, icone=icone, status=1)
        return JsonResponse({'success': True, 'id': conta.id, 'nome_conta': conta.nome_conta})
    except ContaTipo.DoesNotExist:
        return JsonResponse({'error': 'Tipo de conta inválido'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@api_login_required
@require_http_methods(["POST"])
def api_editar_conta(request, user_id, id):
    try:
        data = json.loads(request.body)
        nome_conta = data.get('name', '').strip()
        tipo_conta_id = data.get('type_id')
        icone = data.get('icon_id')

        if not nome_conta or not tipo_conta_id:
            return JsonResponse({'error': 'Dados inválidos ou incompletos.'}, status=400)

        conta = Conta.objects.get(id=id, idusuario=user_id, status=1)
        tipo_conta = ContaTipo.objects.get(id=tipo_conta_id, idusuario=user_id, status=1)
        
        conta.nome_conta = nome_conta
        conta.tipo_conta = tipo_conta
        conta.icone = icone
        conta.save()

        return JsonResponse({'success': True, 'message': 'Conta atualizada com sucesso!', 'id': conta.id, 'nome_conta': conta.nome_conta})
    except Conta.DoesNotExist:
        return JsonResponse({'error': 'Conta não encontrada.'}, status=404)
    except ContaTipo.DoesNotExist:
        return JsonResponse({'error': 'Tipo de conta selecionado é inválido.'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@api_login_required
@require_http_methods(["DELETE"])
def api_excluir_conta(request, user_id, id):
    try:
        conta = Conta.objects.get(id=id, idusuario=user_id, status=1)
        conta.status = 0
        conta.data_removido = datetime.now()
        conta.save()
        return JsonResponse({'success': True, 'message': 'Conta excluída com sucesso.'})
    except Conta.DoesNotExist:
        return JsonResponse({'error': 'Conta não encontrada ou já excluída.'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)