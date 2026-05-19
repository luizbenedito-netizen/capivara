document.getElementById('teste').addEventListener('click', async () => {

    try {
        
        const response = await fetch(`/api/home/constasv/`);
        const dadosContas = await response.json();

        const contas = dadosContas || [];
        
        if (contas.length === 0) {
            alert("Nenhuma carteira encontrada. Crie uma carteira antes de continuar.");
            return;
        }

        // Monta a string visual das contas disponíveis
        let listaContasTexto = contas.map(c => `${c.id} - ${c.nome_conta}`).join('\n');

        // 2. Menu Principal
        const opcao = prompt("Escolha uma opção:\n1 - Criar Despesa\n2 - Adicionar Receita");

        if (opcao === '2') {
            // --- FLUXO DE RECEITA ---
            const valor = prompt("Digite o valor da receita (Use ponto para decimais, ex: 150.50):");
            if (!valor) return;

            const contaId = prompt(`Digite o ID da carteira pertencente:\n\nCarteiras disponíveis:\n${listaContasTexto}`);
            if (!contaId) return;

            // O model 'Receita' exige 'tipo_receita'.
            const tipoReceita = prompt("Digite o tipo da receita (Ex: Salário, Freelance, Pix):", "Geral");

            // Envia via POST
            const formData = new FormData();
            formData.append('valor', valor);
            formData.append('conta_id', contaId);
            formData.append('tipo_receita', tipoReceita);

            const res = await fetch(`/api/home/receitas/criar/`, {
                method: 'POST',
                headers: { 'X-CSRFToken': getCookie('csrftoken') },
                body: formData
            });
            
            const resultado = await res.json();
            if (resultado.success) {
                alert("Receita adicionada com sucesso!");
                location.reload();
            }
            else alert("Erro ao adicionar receita: " + resultado.error);

        } else if (opcao === '1') {
            // --- FLUXO DE DESPESA ---
            const nome = prompt("Nome da despesa:");
            if (!nome) return;

            const tipo = prompt("Tipo da despesa (Sugestões: Alimentação, Transporte, Lazer, Saúde):", "Outros");
            
            //const subgrupo = prompt("Subgrupo (Opcional - Deixe em branco se não houver):");
            const subgrupo = "";
            
            const valor = prompt("Valor da despesa:");
            if (!valor) return;

            const dataVencimento = new Date().toISOString().split('T')[0];

            // const dataVencimento = prompt("Data de vencimento (Formato: AAAA-MM-DD):");
            // if (!dataVencimento) return;

            //const descricao = prompt("Descrição (Opcional):");
            const descricao = "";
            
            // const contaId = prompt(`Digite o ID da conta de origem:\n\nCarteiras disponíveis:\n${listaContasTexto}`);
            // if (!contaId) return;
            const contaId = null;

            const formData = new FormData();
            formData.append('nome', nome);
            formData.append('tipo', tipo);
            formData.append('subgrupo', subgrupo);
            formData.append('valor', valor);
            formData.append('data_vencimento', dataVencimento);
            formData.append('descricao', descricao);
            formData.append('conta_id', contaId);

            const res = await fetch(`/api/home/despesas/criar/`, {
                method: 'POST',
                headers: { 'X-CSRFToken': getCookie('csrftoken') },
                body: formData
            });

            const resultado = await res.json();
            if (resultado.success) {
                alert("Despesa adicionada com sucesso!");
                location.reload();
            }
            else alert("Erro ao adicionar despesa: " + resultado.error);
        }

    } catch (erro) {
        console.error(erro);
        alert("Ocorreu um erro de comunicação com a API.");
    }
});

async function removerDespesa(despesaId) {
    if (!confirm("Deseja realmente remover esta despesa?")) return;

    try {
        const res = await fetch(`/api/home/despesas/remover/${despesaId}/`, {
            method: 'POST',
            headers: { 'X-CSRFToken': getCookie('csrftoken') }
        });
        const dados = await res.json();
        if (dados.success) {
            window.location.reload();
        } else {
            alert("Erro: " + dados.error);
        }
    } catch (e) {
        alert("Erro na comunicação com o servidor.");
    }
}

document.addEventListener('DOMContentLoaded', () => {
    // --- EVENTO: REMOVER RECEITA ---
    document.querySelectorAll('.success-btn').forEach(btn => {
        btn.addEventListener('click', async (e) => {
            const container = e.target.closest('.account-item');
            const receitaId = container.getAttribute('data-id');
            
            if (!receitaId || !confirm("Deseja realmente remover esta receita?")) return;

            try {
                const res = await fetch(`/api/home/receitas/remover/${receitaId}/`, {
                    method: 'POST',
                    headers: { 'X-CSRFToken': getCookie('csrftoken') }
                });
                const dados = await res.json();
                if (dados.success) window.location.reload();
                else alert("Erro: " + dados.error);
            } catch (err) {
                alert("Erro ao remover receita.");
            }
        });
    });

    // --- EVENTO: PAGAR E REMOVER DESPESAS PENDENTES ---
    document.querySelectorAll('.account-actions').forEach(actionsContainer => {
        const despesaId = actionsContainer.getAttribute('data-id');
        if (!despesaId) return;

        // Mapeia os botões pendentes baseado no texto interno deles
        const botoes = actionsContainer.querySelectorAll('.pending-btn');
        
        botoes.forEach(btn => {
            const acao = btn.textContent.trim().toLowerCase();

            if (acao === 'pagar') {
                btn.addEventListener('click', async () => {
                    // 1. Busca as carteiras dinamicamente para o usuário saber qual escolher
                    try {
                        const responseContas = await fetch('/api/home/constasv/');
                        const contas = await responseContas.json();
                        let listaTexto = contas.map(c => `ID: ${c.id} - ${c.nome_conta}`).join('\n');

                        // 2. Abre o prompt pedindo o ID da carteira pagadora
                        const contaId = prompt(`Informe o ID da conta que vai pagar esta despesa:\n\nContas Disponíveis:\n${listaTexto}`);
                        if (!contaId) return;

                        // 3. Envia para a API de pagamento
                        const formData = new FormData();
                        formData.append('conta_id', contaId);

                        const res = await fetch(`/api/home/despesas/pagar/${despesaId}/`, {
                            method: 'POST',
                            headers: { 'X-CSRFToken': getCookie('csrftoken') },
                            body: formData
                        });
                        
                        const dados = await res.json();
                        if (dados.success) {
                            window.location.reload();
                        } else {
                            alert("Não foi possível pagar: " + dados.error);
                        }
                    } catch (err) {
                        alert("Erro ao processar pagamento.");
                    }
                });
            } 
            
            else if (acao === 'remover') {
                // Atribui a mesma função de remover para a despesa que ainda está pendente
                btn.addEventListener('click', () => removerDespesa(despesaId));
            }
        });
    });
});