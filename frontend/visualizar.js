// Exibe o nome do usuário logado no topo
const username = localStorage.getItem("username");

if (username) {
  const usuarioLogado = document.getElementById("usuario-logado");
  if (usuarioLogado) {
    usuarioLogado.innerHTML = `<strong>${username}</strong>`;
  }
} else {
  // Se não estiver logado, redireciona para o login
  window.location.href = "index.html";
}

// Função de logoff
function logout() {
  localStorage.clear();
  window.location.href = "index.html";
}

document.addEventListener("DOMContentLoaded", () => {
  const tabela = document.getElementById("tabela-registros");
  const filtroInput = document.getElementById("filtro-nome");
  const menuContexto = document.getElementById("menu-contexto");
  const modalConfirmacao = document.getElementById("modal-confirmacao");
  const modalImportacao = document.getElementById("modal-importacao");
  const btnConfirmarExclusao = document.getElementById("btn-confirmar-exclusao");
  const btnCancelarExclusao = document.getElementById("btn-cancelar-exclusao");
  const btnConfirmarImportacao = document.getElementById("btn-confirmar-importacao");
  const btnCancelarImportacao = document.getElementById("btn-cancelar-importacao");

  window.registros = [];

  async function carregarRegistros() {
    try {
      const resposta = await fetch("/api/registros");
      window.registros = await resposta.json();
      preencherTabela(window.registros);
    } catch (erro) {
      mostrarAlerta("Erro ao carregar registros", "erro");
      console.error(erro);
    }
  }

  function preencherTabela(lista) {
    tabela.innerHTML = "";

    lista.forEach((registro) => {
      const linha = document.createElement("tr");
      linha.dataset.idPessoa = registro.id_pessoa;

        const formatarData = (dataISO) => {
        if (!dataISO) return "";
        const [ano, mes, dia] = dataISO.split("-");
        return `${dia}/${mes}/${ano}`;
      };
      linha.innerHTML = `
        <td>${registro.cpf || ""}</td>
        <td>${registro.nome || ""}</td>
        <td>${registro.codigo_procedimento || ""}</td>
        <td>${registro.nome_procedimento || ""}</td>
        <td>${registro.data_proc || ""}</td>
        <td>${registro.cid || ""}</td>
      `;
      tabela.appendChild(linha);
    });
  }

  filtroInput.addEventListener("input", () => {
    const termo = filtroInput.value.trim().toLowerCase();

    const filtrados = window.registros.filter((r) => {
      return (
        (r.nome || "").toLowerCase().includes(termo) ||
        (r.cpf || "").toLowerCase().includes(termo) ||
        (r.cns || "").toLowerCase().includes(termo)
      );
    });

    preencherTabela(filtrados);
  });

  tabela.addEventListener("contextmenu", (event) => {
    event.preventDefault();
    const linha = event.target.closest("tr");
    if (!linha) return;

    document
      .querySelectorAll("tr.selecionado")
      .forEach((tr) => tr.classList.remove("selecionado"));
    linha.classList.add("selecionado");

    const idPessoa = linha.dataset.idPessoa;
    if (!idPessoa) return;

    menuContexto.dataset.idPessoa = idPessoa;

    const menuWidth = 160;
    const menuHeight = 120;
    const maxLeft = window.innerWidth - menuWidth;
    const maxTop = window.innerHeight - menuHeight;

    const posX = Math.min(event.pageX, maxLeft);
    const posY = Math.min(event.pageY, maxTop);

    menuContexto.style.left = `${posX}px`;
    menuContexto.style.top = `${posY}px`;
    menuContexto.style.display = "block";
  });

  window.editarSelecionado = function () {
    const id = menuContexto.dataset.idPessoa;
    if (!id) return;

    const registro = window.registros.find((r) => r.id_pessoa == id);
    if (!registro) return;

    localStorage.setItem("registroEditavel", JSON.stringify(registro));
    window.location.href = "crud.html";
  };

  window.verDetalhes = function () {
    const id = menuContexto.dataset.idPessoa;
    if (!id) return;

    const registro = window.registros.find((r) => r.id_pessoa == id);
    if (!registro) return;

    document.getElementById("titulo-procedimento").textContent =
      registro.codigo_procedimento || "Procedimento";
    document.getElementById("nome-procedimento-detalhe").textContent =
      registro.nome_procedimento || "—";

    const valorFormatado = formatarMoeda(registro.vlr_procedimento);
    document.getElementById("valor-procedimento-detalhe").textContent =
      valorFormatado;

    document.getElementById("janela-detalhes").style.display = "flex";
  };

  // Disponibiliza fecharDetalhes globalmente para o onclick do HTML
  window.fecharDetalhes = function () {
    document.getElementById("janela-detalhes").style.display = "none";
  };

  function formatarMoeda(valor) {
    if (!valor) return "R$ 0,00";
    return Number(valor).toLocaleString("pt-BR", {
      style: "currency",
      currency: "BRL",
    });
  }

  window.exportarSelecionado = function () {
    const id = menuContexto.dataset.idPessoa;
    if (!id) return;
    mostrarAlerta(`Exportar dados do registro ${id}`, "info");
  };

  window.importarSelecionado = function () {
    modalImportacao.style.display = "flex";
  };

  btnCancelarImportacao.addEventListener("click", () => {
    modalImportacao.style.display = "none";
  });

  btnConfirmarImportacao.addEventListener("click", async () => {
    const input = document.getElementById("arquivo-importacao");
    const arquivo = input.files[0];

    if (!arquivo) {
      mostrarAlerta("Selecione um arquivo para importar.", "erro");
      return;
    }

    const formData = new FormData();
    formData.append("arquivo", arquivo);

    try {
      const resposta = await fetch("/api/importar", {
        method: "POST",
        body: formData,
      });

      // O endpoint pode retornar CSV em caso de erro. Tente JSON e, se falhar, ignore parse.
      let resultado = null;
      try {
        resultado = await resposta.json();
      } catch (_) {
        resultado = null;
      }

      if (resposta.ok) {
        mostrarAlerta("Importação concluída com sucesso!", "sucesso");
        if (resultado && resultado.erros && resultado.erros.length > 0) {
          console.warn("Erros na importação:", resultado.erros);
        }
        carregarRegistros();
      } else {
        const msg =
          (resultado && resultado.erro) ||
          "Erro na importação. Verifique o arquivo de retorno (CSV).";
        mostrarAlerta(msg, "erro");
      }
    } catch (erro) {
      mostrarAlerta("Erro ao enviar arquivo.", "erro");
      console.error(erro);
    }

    modalImportacao.style.display = "none";
  });

  window.excluirSelecionado = function () {
    const id = menuContexto.dataset.idPessoa;
    if (!id) return;

    btnConfirmarExclusao.dataset.idPessoa = id;
    modalConfirmacao.style.display = "flex";
  };

  btnConfirmarExclusao.addEventListener("click", async function () {
    const id = this.dataset.idPessoa;
    if (!id) return;

    try {
      const resposta = await fetch(`/api/registros/${id}`, {
        method: "DELETE",
      });

      if (resposta.ok) {
        mostrarAlerta("Registro excluído com sucesso!", "sucesso");
        menuContexto.style.display = "none";
        carregarRegistros();
      } else {
        mostrarAlerta("Erro ao excluir registro.", "erro");
      }
    } catch (erro) {
      mostrarAlerta("Erro de conexão ao excluir.", "erro");
      console.error(erro);
    }

    modalConfirmacao.style.display = "none";
  });

  btnCancelarExclusao.addEventListener("click", function () {
    modalConfirmacao.style.display = "none";
  });

  document.addEventListener("click", (e) => {
    if (!e.target.closest("tr") && !e.target.closest("#menu-contexto")) {
      document
        .querySelectorAll("tr.selecionado")
        .forEach((tr) => tr.classList.remove("selecionado"));
      menuContexto.style.display = "none";
    }
  });

  carregarRegistros();
});

function mostrarAlerta(mensagem, tipo = "info") {
  const alerta = document.getElementById("alerta-app");
  if (!alerta) return;

  alerta.textContent = mensagem;
  alerta.className = `alerta-app ${tipo}`;
  alerta.style.display = "block";

  setTimeout(() => {
    alerta.style.display = "none";
  }, 4000);
}

function exportarTodos() {
  if (!window.registros || window.registros.length === 0) {
    mostrarAlerta("Nenhum registro disponível para exportação.", "erro");
    return;
  }

  // Cabeçalho fixo
  let conteudo = "ID | Nome | CPF | Data de Nascimento\n";

  // Linhas dos registros
  window.registros.forEach((r) => {
    const linha = `${r.id_pessoa} | ${r.nome} | ${r.cpf} | ${r.dt_nascimento}`;
    conteudo += linha + "\n";
  });

  // Cria o arquivo .txt
  const blob = new Blob([conteudo], { type: "text/plain;charset=utf-8" });
  const url = URL.createObjectURL(blob);

  // Cria link para download
  const a = document.createElement("a");
  a.href = url;
  a.download = "registros_exportados.txt";
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}
