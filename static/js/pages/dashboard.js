document.addEventListener('DOMContentLoaded', async () => {
    await carregarGraficoDespesas();
});

async function carregarGraficoDespesas() {

    try {

        const response = await fetch('/api/dashboard/despesas-categorias/');
        const data = await response.json();

        if (!data.success) {
            console.error(data.error);
            return;
        }

        const ctx = document.getElementById('expenseChart');

        new Chart(ctx, {
            type: 'doughnut',

            data: {
                labels: data.labels,

                datasets: [{
                    label: 'Despesas',
                    data: data.valores,

                    borderWidth: 0,

                    hoverOffset: 12
                }]
            },

            options: {

                responsive: true,
                maintainAspectRatio: false,

                animation: {
                    animateRotate: true,
                    animateScale: true,
                    duration: 1200
                },

                plugins: {

                    legend: {
                        position: 'bottom'
                    },

                    tooltip: {
                        callbacks: {
                            label: function(context) {

                                const value = context.raw;

                                return new Intl.NumberFormat('pt-BR', {
                                    style: 'currency',
                                    currency: 'BRL'
                                }).format(value);
                            }
                        }
                    }
                }
            }
        });

    } catch (error) {
        console.error(error);
    }
}



document.addEventListener('DOMContentLoaded', async () => {

    await carregarGraficoReceitasDespesas();

});

async function carregarGraficoReceitasDespesas() {

    try {

        const response = await fetch('/api/dashboard/receitas-despesas/');
        const data = await response.json();

        if (!data.success) {
            console.error(data.error);
            return;
        }

        const ctx = document.getElementById('incomeExpenseChart');

        new Chart(ctx, {

            type: 'bar',

            data: {

                labels: data.labels,

                datasets: [{

                    data: data.valores,

                    borderRadius: 10,

                    borderSkipped: false

                }]
            },

            options: {

                responsive: true,

                maintainAspectRatio: false,

                animation: {
                    duration: 1400
                },

                plugins: {

                    legend: {
                        display: false
                    },

                    tooltip: {

                        callbacks: {

                            label: function(context) {

                                return new Intl.NumberFormat('pt-BR', {
                                    style: 'currency',
                                    currency: 'BRL'
                                }).format(context.raw);
                            }
                        }
                    }
                },

                scales: {

                    y: {

                        beginAtZero: true,

                        ticks: {

                            callback: function(value) {

                                return new Intl.NumberFormat('pt-BR', {
                                    style: 'currency',
                                    currency: 'BRL'
                                }).format(value);
                            }
                        }
                    }
                }
            }
        });

    } catch (error) {

        console.error(error);

    }
}