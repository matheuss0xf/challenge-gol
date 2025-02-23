let chartInstance = null;

document.addEventListener('DOMContentLoaded', () => {
    const userName = localStorage.getItem('userName');

    if (userName) {
        document.getElementById('userName').textContent = userName;
    } else {
        document.getElementById('userName').textContent = '';
    }
});

async function fetchData() {
    const startDate = document.getElementById('startDate').value;
    const endDate = document.getElementById('endDate').value;
    const market = document.getElementById('market').value.trim();

    let flightDateParam = '';
    if (startDate || endDate) {
        flightDateParam = `${formatDateParam(startDate)};${formatDateParam(endDate)}`
            .replace(/;+$/, '')
            .replace(/^;/, '');
    }

    const params = new URLSearchParams({
        market: market,
        flight_date: flightDateParam,
        sort: 'year:asc,month:asc'
    });

    // Faz a requisição à API
    const response = await fetch(`/api/flights?${params}`, {
        credentials: 'include',
    });

    if (!response.ok) {
        throw new Error(await response.text());
    }

    const flights = await response.json();
    updateTable(flights);
    updateChart(flights);

}

// Função para atualizar a tabela com os dados dos voos
function updateTable(flights) {
    const tbody = document.getElementById('flightData');
    tbody.innerHTML = flights.map(flight => `
        <tr>
            <td>${flight.mercado}</td>
            <td>${flight.ano}</td>
            <td>${flight.mes.toString().padStart(2, '0')}</td>
            <td>${flight.rpk.toLocaleString('pt-BR')}</td>
        </tr>
    `).join('');
}

function updateChart(flights) {
    const ctx = document.getElementById('flightChart').getContext('2d');

    if (chartInstance) {
        chartInstance.destroy();
    }

    chartInstance = new Chart(ctx, {
        type: 'line',
        data: {
            labels: flights.map(f => `${f.ano}-${f.mes.toString().padStart(2, '0')}`),
            datasets: [{
                label: 'RPK (Quantidade de passageiros pagos transportados * km voados.)',
                data: flights.map(f => f.rpk),
                borderColor: '#0d6efd',
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top',
                }
            },
            scales: {
                y: {
                    title: {
                        display: true,
                        text: 'RPK (em milhões)',
                        color: '#666'
                    },
                    ticks: {
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Período',
                        color: '#666'
                    }
                }
            }
        }
    });
}

function formatDateParam(dateString) {
    if (!dateString) return '';
    return dateString.replace('-', '/'); 
}