async function carregarDashboard() {
  try {
    // Dados fictícios para apresentação
    const dados = {
      total_exames: 1250,
      valor_total: 45800.75,
      pacientes_ativos: 320,
      grupos: [
        { grupo: "Hematologia", quantidade: 300, percentual: 24, valor: 12000 },
        { grupo: "Bioquímica", quantidade: 250, percentual: 20, valor: 9500 },
        { grupo: "Imunologia", quantidade: 200, percentual: 16, valor: 7800 },
        { grupo: "Microbiologia", quantidade: 150, percentual: 12, valor: 6200 },
        { grupo: "Imagem", quantidade: 350, percentual: 28, valor: 10300 }
      ]
    };

    // Preenche os cards
    document.getElementById("card-total-exames").textContent = dados.total_exames;
    document.getElementById("card-valor-total").textContent =
      `R$ ${dados.valor_total.toLocaleString("pt-BR", { minimumFractionDigits: 2 })}`;
    document.getElementById("card-pacientes-ativos").textContent = dados.pacientes_ativos;

    // Gráfico 1 - Linha
    const config1 = {
      type: 'line',
      data: {
        labels: dados.grupos.map(g => g.grupo),
        datasets: [{
          label: 'Quantidade de Exames',
          data: dados.grupos.map(g => g.quantidade),
          borderColor: '#00ffff',
          backgroundColor: '#00ffff44',
          fill: true,
          tension: 0.4
        }]
      },
      options: {
        plugins: { legend: { labels: { color: '#00ffff' } } },
        scales: {
          x: { ticks: { color: '#00ffffaa' } },
          y: { ticks: { color: '#00ffffaa' } }
        }
      }
    };

    // Gráfico 2 - Rosquinha
    const config2 = {
      type: 'doughnut',
      data: {
        labels: dados.grupos.map(g => g.grupo),
        datasets: [{
          data: dados.grupos.map(g => g.percentual),
          backgroundColor: ['#00ffff', '#00aaff', '#0077aa', '#004466', '#002233'],
          borderColor: '#001f33',
          borderWidth: 2
        }]
      },
      options: {
        plugins: { legend: { labels: { color: '#00ffff' } } }
      }
    };

    // Gráfico 3 - Barras
    const config3 = {
      type: 'bar',
      data: {
        labels: dados.grupos.map(g => g.grupo),
        datasets: [{
          label: 'Valor por Grupo (R$)',
          data: dados.grupos.map(g => g.valor),
          backgroundColor: '#00ffff88',
          borderColor: '#00ffff',
          borderWidth: 1
        }]
      },
      options: {
        plugins: { legend: { labels: { color: '#00ffff' } } },
        scales: {
          x: { ticks: { color: '#00ffffaa' } },
          y: { ticks: { color: '#00ffffaa' } }
        }
      }
    };

    // Renderiza os gráficos
    new Chart(document.getElementById('grafico1'), config1);
    new Chart(document.getElementById('grafico2'), config2);
    new Chart(document.getElementById('grafico3'), config3);

  } catch (erro) {
    console.error("Erro ao carregar dashboard:", erro);
  }
}

document.addEventListener("DOMContentLoaded", carregarDashboard);
