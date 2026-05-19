// ==========================================
// 1. CAMADA DE SERVIÇOS (SOLID - Responsabilidade Única)
// ==========================================

// Centraliza e padroniza as chamadas de alertas (Evita duplicação do Boilerplate do Swal)
const AlertService = {
    config: {
        position: 'top',
        customClass: { popup: 'custom-confirm' }
    },
    close() { 
        Swal.close(); 
    },
    success(title) { 
        return Swal.fire({ ...this.config, icon: 'success', title }); 
    },
    error(title) { 
        return Swal.fire({ ...this.config, icon: 'error', title }); 
    },
    warn(title) { 
        return Swal.fire({ ...this.config, icon: 'warning', title }); 
    },
    async confirm(title, text = "") {
        const result = await Swal.fire({
            ...this.config,
            title,
            text,
            icon: 'warning',
            showCancelButton: true,
            confirmButtonText: 'Sim',
            cancelButtonText: 'Cancelar',
            reverseButtons: true
        });
        return result.isConfirmed;
    }
};

// Requisições API
const ApiService = {
    getHeaders(contentType = 'application/json') {
        const headers = { 'X-CSRFToken': getCookie('csrftoken') };
        if (contentType) headers['Content-Type'] = contentType;
        return headers;
    },
    async buscarTiposConta() {
        const response = await fetch('/api/heart/tipos_conta/');
        return response.json();
    },
    async excluirTipoConta(id) {
        return fetch(`/api/heart/tipos_conta/${id}/`, {
            method: 'DELETE',
            headers: this.getHeaders(null)
        });
    },
    async criarTipoConta(tipoConta) {
        return fetch('/api/heart/criar_tipo_conta/', {
            method: 'POST',
            headers: this.getHeaders('application/x-www-form-urlencoded'),
            body: new URLSearchParams({ tipo_conta: tipoConta })
        });
    },
    async criarConta(tipoContaId, nomeConta, tipoIcone) {
        return fetch('/api/heart/criar_conta/', {
            method: 'POST',
            headers: this.getHeaders('application/json'),
            body: JSON.stringify({ tipo_conta: tipoContaId, nome_conta: nomeConta, icone: tipoIcone })
        });
    },
    async obterDetalhesConta(accountId) {
        return fetch(`/api/heart/obter_detalhes_conta/${accountId}`);
    },
    async editarConta(accountId, nome, tipoContaId, iconeId) {
        return fetch(`/api/heart/editar_conta/${accountId}/`, {
            method: 'POST',
            headers: this.getHeaders('application/json'),
            body: JSON.stringify({ name: nome, type_id: tipoContaId, icon_id: iconeId })
        });
    },
    async excluirConta(accountId) {
        return fetch(`/api/heart/excluir_conta/${accountId}/`, {
            method: 'DELETE',
            headers: this.getHeaders(null)
        });
    }
};

// ==========================================
// 2. CONTROLE DO MODAL PRINCIPAL (DOM)
// ==========================================

document.addEventListener("DOMContentLoaded", function () {
    const modal = document.querySelector('.modal-custom-account');
    if (!modal) return;

    const accountDropdown = modal.querySelector('#account_type_dropdown');
    const iconDropdown = modal.querySelector('#icon_dropdown');

    // Renderiza a lista de tipos de conta dinamicamente
    const renderTiposConta = (data) => {
        accountDropdown.querySelectorAll('.dynamic-option').forEach(el => el.remove());
        
        let html = '';
        data.forEach(item => {
            html += `
                <li class="dropdown-option d-flex gap-2 dynamic-option">
                    <button class="dropdown-item py-2 d-flex" data-value="${item.id}">
                        ${item.tipo_conta}
                    </button>
                    <span class="btn-outline-danger d-flex align-items-center justify-content-center delete-option-btn" 
                          data-id="${item.id}" data-name="${item.tipo_conta}">
                        <i class="fa-minus"></i>
                    </span>
                </li>
            `;
        });

        const divider = accountDropdown.querySelector('.dropdown-divider').parentElement;
        divider.insertAdjacentHTML('beforebegin', html);
        bindDeleteButtons();
    };

    const atualizarTiposConta = async () => {
        try {
            const data = await ApiService.buscarTiposConta();
            renderTiposConta(data);
        } catch (err) {
            console.error("Erro ao atualizar listagem:", err);
        }
    };

    // Vincula o evento de exclusão nos botões do dropdown de tipo de conta
    const bindDeleteButtons = () => {
        accountDropdown.querySelectorAll('.delete-option-btn').forEach(btn => {
            btn.addEventListener('click', async (e) => {
                e.preventDefault();
                e.stopPropagation();

                const { id, name: nome } = btn.dataset;
                AlertService.close();

                const confirmado = await AlertService.confirm(`Deseja realmente excluir "${nome}"?`);
                if (!confirmado) {
                    showModal({ name: 'modal-wallets' });
                    return;
                }

                try {
                    const response = await ApiService.excluirTipoConta(id);
                    if (!response.ok) throw new Error();

                    await AlertService.success('Conta removida com sucesso.');
                    await resetDropdown(accountDropdown);
                    await atualizarTiposConta();
                } catch (err) {
                    console.error(err);
                    await AlertService.error('Não foi possível excluir.');
                } finally {
                    showModal({ name: 'modal-wallets' });
                }
            });
        });
    };

    // Inicializa a criação rápida de novos tipos de conta dentro do dropdown
    const initAddAccountType = () => {
        const btn = modal.querySelector('#add_account_btn');
        const input = modal.querySelector('#add_account');
        if (!btn || !input) return;

        btn.addEventListener('click', async () => {
            const tipoConta = input.value.trim();
            if (!tipoConta) return;

            try {
                const response = await ApiService.criarTipoConta(tipoConta);
                const data = await response.json();

                if (!response.ok) {
                    alert(data.error || 'Erro ao criar');
                    return;
                }

                input.value = '';
                atualizarTiposConta();
            } catch (error) {
                console.error(error);
                alert('Erro interno');
            }
        });
    };

    // Evento do botão salvar
    const initSaveAccount = () => {
        const saveBtn = modal.querySelector('#account_type_save');
        if (!saveBtn) return;

        saveBtn.addEventListener('click', async () => {
            const tipoContaId = accountDropdown.querySelector('#tipoConta')?.dataset?.value;
            const tipoIcone = iconDropdown.querySelector('#icone')?.dataset?.value;
            const nomeConta = modal.querySelector('.account-name')?.value?.trim();

            if (!tipoContaId || !nomeConta || !tipoIcone) {
                await AlertService.warn('Preencha todos os campos');
                await showModal({ name: 'modal-wallets' });
                return;
            }

            const confirmado = await AlertService.confirm('Deseja realmente salvar esta conta?');
            if (!confirmado) return;

            try {
                const response = await ApiService.criarConta(tipoContaId, nomeConta, tipoIcone);
                if (!response.ok) throw new Error();

                await AlertService.success('Conta criada com sucesso.');
                location.reload();
            } catch (error) {
                console.error(error);
                await AlertService.error('Não foi possível salvar.');
            }
        });
    };

    // Gatilhos de Inicialização
    initAddAccountType();
    initSaveAccount();
    atualizarTiposConta();
});

// ==========================================
// 3. FUNÇÕES GLOBAIS
// ==========================================

window.abrirModalConta = function(accountId = null) {
    const isEditMode = accountId !== null;
    
    showModal({
        name: 'modal-wallets',
        before: async ({ body: popup }) => {
            const titleElem = popup.querySelector('#modal-account-title');
            const deleteBtn = popup.querySelector('#account_delete_btn');
            const saveNewBtn = popup.querySelector('#account_type_save');
            const saveEditBtn = popup.querySelector('#account_type_edit_save');
            const nameInput = popup.querySelector('.account-name');
            const accountDropdown = popup.querySelector('#account_type_dropdown');
            const iconDropdown = popup.querySelector('#icon_dropdown');

            if (isEditMode) {
                titleElem.textContent = "Editar Conta";
                deleteBtn.classList.remove('d-none');
                saveNewBtn.classList.add('d-none');
                saveEditBtn.classList.remove('d-none');

                try {
                    const response = await ApiService.obterDetalhesConta(accountId);
                    if (!response.ok) throw new Error('Erro ao buscar dados do servidor');
                    
                    const data = await response.json();
                    nameInput.value = data.nome_conta;

                    const typeOption = accountDropdown.querySelector(`[data-value="${data.tipo_conta_id}"]`) || 
                                       accountDropdown.querySelector(`[data-id="${data.tipo_conta_id}"]`);
                    if (typeOption) typeOption.click();

                    const iconOption = iconDropdown.querySelector(`.icon-option[data-value="${data.icone}"]`);
                    if (iconOption) iconOption.click();

                    document.activeElement.blur();
                } catch (error) {
                    console.error("Erro ao popular modal de edição:", error);
                }

                saveEditBtn.onclick = () => executarSalvarEdicao(accountId, popup);
                deleteBtn.onclick = () => executarExclusao(accountId);
            } else {
                titleElem.textContent = "Criar Conta";
                deleteBtn.classList.add('d-none');
                saveNewBtn.classList.remove('d-none');
                saveEditBtn.classList.add('d-none');
                
                nameInput.value = '';
                if (typeof window.resetDropdown === "function") {
                    window.resetDropdown(accountDropdown);
                    window.resetDropdown(iconDropdown);
                }
            }
        }
    });
};

async function executarSalvarEdicao(accountId, popup) {
    const nome = popup.querySelector('.account-name').value;
    const tipoContaId = popup.querySelector('#tipoConta').getAttribute('data-value');
    const iconeId = popup.querySelector('#icone').getAttribute('data-value');

    try {
        const response = await ApiService.editarConta(accountId, nome, tipoContaId, iconeId);
        if (response.ok) {
            await AlertService.success('Atualizado com sucesso!');
            await location.reload();
        } else {
            await AlertService.error('Não foi possível atualizar');
        }
    } catch (error) {
        console.error(error);
    }
}

async function executarExclusao(accountId) {
    const confirmado = await AlertService.confirm('Tem certeza?', 'Esta ação não poderá ser desfeita!');
    if (!confirmado) return;

    try {
        const response = await ApiService.excluirConta(accountId);
        if (response.ok) {
            await AlertService.success('Conta removida com sucesso.');
            await location.reload();
        } else {
            await AlertService.error('Não foi possível excluir');
        }
    } catch (error) {
        console.error(error);
    }
}