// Exibe o nome do usuário logado no topo
const username = localStorage.getItem("username");

if (username) {
  const usuarioLogado = document.getElementById("usuario-logado");
  if (usuarioLogado) {
    usuarioLogado.innerHTML = `<strong>${username}</strong>`;
  }
} else {
  window.location.href = "index.html";
}

function logout() {
  localStorage.clear();
  window.location.href = "index.html";
}

document.addEventListener("DOMContentLoaded", () => {
  const formRegistro = document.getElementById("form-registro");
  const btnSalvar = document.getElementById("btn-salvar");
  const btnNovo = document.getElementById("btn-novo");
  const btnExcluir = document.getElementById("btn-excluir");

  const registro = localStorage.getItem("registroEditavel");
  if (registro) {
    preencherFormulario(JSON.parse(registro));
    localStorage.removeItem("registroEditavel");
  }

  function preencherFormulario(registro) {
    document.getElementById("cns").value = registro.cns || "";
    document.getElementById("nome").value = registro.nome || "";
    document.getElementById("sexo").value = registro.sexo || "";
    document.getElementById("cpf").value = registro.cpf || "";
    document.getElementById("dt_nascimento").value = registro.dt_nascimento || "";
    document.getElementById("raca").value = registro.raca || "";
    document.getElementById("nacionalidade").value = registro.nacionalidade || "";
    document.getElementById("cep").value = registro.cep || "";
    document.getElementById("tipo_logradouro").value = registro.tipo_logradouro || "";
    document.getElementById("nome_logradouro").value = registro.nome_logradouro || "";
    document.getElementById("numero").value = registro.numero || "";
    document.getElementById("complemento").value = registro.complemento || "";
    document.getElementById("bairro").value = registro.bairro || "";
    document.getElementById("cidade").value = registro.cidade || "";
    document.getElementById("uf").value = registro.uf || "";
    document.getElementById("ddd").value = registro.ddd || "";
    document.getElementById("telefone").value = registro.telefone || "";
    document.getElementById("ibge").value = registro.ibge || "";
    document.getElementById("data_proc").value = registro.data_proc?.substring(0, 10) || "";
    document.getElementById("codigo_procedimento").value = registro.codigo_procedimento || "";
    document.getElementById("nome_procedimento").value = registro.nome_procedimento || "";
    document.getElementById("quantidade").value = registro.quantidade || "";
    document.getElementById("cid").value = registro.cid || "";
    document.getElementById("carater_atendimento").value = registro.carater_atendimento || "";

    formRegistro.dataset.idPessoa = registro.id_pessoa;
  }

  btnSalvar.addEventListener("click", () => {
    formRegistro.requestSubmit();
  });

  btnNovo.addEventListener("click", () => {
    formRegistro.reset();
    delete formRegistro.dataset.idPessoa;
    mostrarAlerta("Formulário limpo para novo registro", "info");
  });

  btnExcluir.addEventListener("click", async () => {
    const id = formRegistro.dataset.idPessoa;
    if (!id) {
      mostrarAlerta("Nenhum registro carregado para exclusão", "erro");
      return;
    }

    try {
      const resposta = await fetch(`/api/registros/${id}`, {
        method: "DELETE"
      });

      if (resposta.ok) {
        mostrarAlerta("Registro excluído com sucesso!", "sucesso");
        formRegistro.reset();
        delete formRegistro.dataset.idPessoa;
      } else {
        mostrarAlerta("Erro ao excluir registro.", "erro");
      }
    } catch (erro) {
      mostrarAlerta("Erro de conexão ao excluir.", "erro");
    }
  });

  formRegistro.addEventListener("submit", async function (e) {
    e.preventDefault();

    const id = this.dataset.idPessoa;
    const metodo = id ? "PUT" : "POST";
    const url = id
      ? `/api/registros/${id}`
      : `/api/registros`;

    const dados = {
      cns: document.getElementById("cns").value.trim(),
      nome: document.getElementById("nome").value.trim(),
      sexo: document.getElementById("sexo").value.trim(),
      cpf: document.getElementById("cpf").value.trim(),
      dt_nascimento: document.getElementById("dt_nascimento").value.trim(),
      raca: document.getElementById("raca").value.trim(),
      nacionalidade: document.getElementById("nacionalidade").value.trim(),
      cep: document.getElementById("cep").value.trim(),
      tipo_logradouro: document.getElementById("tipo_logradouro").value.trim(),
      nome_logradouro: document.getElementById("nome_logradouro").value.trim(),
      numero: document.getElementById("numero").value.trim(),
      complemento: document.getElementById("complemento").value.trim(),
      bairro: document.getElementById("bairro").value.trim(),
      cidade: document.getElementById("cidade").value.trim(),
      uf: document.getElementById("uf").value.trim(),
      ddd: document.getElementById("ddd").value.trim(),
      telefone: document.getElementById("telefone").value.trim(),
      ibge: document.getElementById("ibge").value.trim(),
      data_proc: document.getElementById("data_proc").value.trim(),
      codigo_procedimento: document.getElementById("codigo_procedimento").value.trim(),
      nome_procedimento: document.getElementById("nome_procedimento").value.trim(),
      quantidade: document.getElementById("quantidade").value.trim(),
      cid: document.getElementById("cid").value.trim(),
      carater_atendimento: document.getElementById("carater_atendimento").value.trim()
    };

    try {
      const resposta = await fetch(url, {
        method: metodo,
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(dados)
      });

      if (resposta.ok) {
        mostrarAlerta("Registro salvo com sucesso!", "sucesso");
        this.reset();
        delete this.dataset.idPessoa;
      } else {
        mostrarAlerta("Erro ao salvar registro.", "erro");
      }
    } catch (erro) {
      mostrarAlerta("Erro de conexão ao salvar.", "erro");
    }
  });
});

function mostrarAlerta(mensagem, tipo = "info") {
  const alerta = document.getElementById("alerta-app");
  alerta.textContent = mensagem;
  alerta.className = `alerta-app ${tipo}`;
  alerta.style.display = "block";

  setTimeout(() => {
    alerta.style.display = "none";
  }, 4000);
}

document.getElementById("cep").addEventListener("blur", async () => {
  const cep = document.getElementById("cep").value.trim();
  if (cep.length === 8) {
    const resposta = await fetch(`/api/cep/${cep}`);
    const dados = await resposta.json();

    document.getElementById("tipo_logradouro").value = dados.tipo_logradouro || "";
    document.getElementById("nome_logradouro").value = dados.nome_logradouro || "";
    document.getElementById("bairro").value = dados.bairro || "";
    document.getElementById("cidade").value = dados.cidade || "";
    document.getElementById("uf").value = dados.uf || "";
    document.getElementById("ibge").value = dados.ibge || "";
  }
});

document.getElementById("codigo_procedimento").addEventListener("blur", async () => {
  const codigo = document.getElementById("codigo_procedimento").value.trim();
  if (codigo.length > 0) {
    const resposta = await fetch(`/api/procedimento/${codigo}`);
    const dados = await resposta.json();

    document.getElementById("nome_procedimento").value = dados.nome_procedimento || "";
  }
});

