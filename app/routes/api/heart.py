from django.urls import path
from app.views.heart.api import mconta
from app.views.heart.api import mcreate

urlpatterns = [
    # (GET)
    path("obter_receita/", mconta.api_obter_receita, name="api_obter_receita"),
    path("contas/", mconta.api_listar_contas, name="api_listar_contas"),
    path("tipos_conta/", mconta.api_listar_tipos_conta, name="api_listar_tipos_conta"),
    path("obter_detalhes_conta/<int:id>/", mconta.api_detalhes_conta, name="api_detalhes_conta"),
    # (POST / DELETE)
    path("criar_tipo_conta/", mconta.api_criar_tipo_conta, name="api_criar_tipo_conta"),
    path("tipos_conta/<int:id>/", mconta.api_excluir_tipo_conta, name="api_excluir_tipo_conta"),
    path("criar_conta/", mconta.api_criar_conta, name="api_criar_conta"),
    path("editar_conta/<int:id>/", mconta.api_editar_conta, name="api_editar_conta"),
    path("excluir_conta/<int:id>/", mconta.api_excluir_conta, name="api_excluir_conta"),
    # MCreate
    path('constasv/', mcreate.buscar_tipos_conta, name='constasv'),
    path('receitas/criar/', mcreate.api_criar_receita, name='api_criar_receita'),
    path('despesas/criar/', mcreate.api_criar_despesa, name='api_criar_despesa'),
    # MCreate
    path('despesas/pagar/<int:despesa_id>/', mcreate.api_pagar_despesa, name='api_pagar_despesa'),
    path('despesas/remover/<int:despesa_id>/', mcreate.api_remover_despesa, name='api_remover_despesa'),
    path('receitas/remover/<int:receita_id>/', mcreate.api_remover_receita, name='api_remover_receita')
]