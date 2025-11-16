async function carregarDashboard() {
  try {
    const resposta = await fetch("http://127.0.0.1:5051/api/dashboard");
    const dados = await resposta.json();

    // Atualiza os cards
    document.getElementById("card-total-exames").textContent = dados.total_exames;
    document.getElementById("card-valor-total").textContent = 
      `R$ ${dados.valor_total.toLocaleString("pt-BR", { minimumFractionDigits: 2 })}`;
    document.getElementById("card-pacientes-ativos").textContent = dados.pacientes_ativos;

    // Gráfico de linha (quantidade por grupo)
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

    // Gráfico de pizza (percentual por grupo)
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

    // Gráfico de barras (valor por grupo)
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

    new Chart(document.getElementById('grafico1'), config1);
    new Chart(document.getElementById('grafico2'), config2);
    new Chart(document.getElementById('grafico3'), config3);

  } catch (erro) {
    console.error("Erro ao carregar dashboard:", erro);
  }
}

document.addEventListener("DOMContentLoaded", carregarDashboard);
