document.addEventListener("DOMContentLoaded", () => {
  // LOGIN
  const loginForm = document.getElementById("loginForm");
  if (loginForm) {
    loginForm.addEventListener("submit", async function (e) {
      e.preventDefault();

      const usuarioInput = document.getElementById("usuario");
      const senhaInput = document.getElementById("password");

      if (!usuarioInput || !senhaInput) {
        console.error("Campos de login não encontrados no DOM.");
        return;
      }

      const username = usuarioInput.value.trim();
      const senha = senhaInput.value.trim();

      try {
        const resposta = await fetch("/api/login", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ username, senha })
        });

        const dados = await resposta.json();

        if (resposta.ok) {
          localStorage.setItem("username", dados.usuario.username);
          localStorage.setItem("email", dados.usuario.email);
          window.location.href = "visualizar.html";
        } else {
          alert(dados.erro || "Erro ao fazer login");
        }
      } catch (erro) {
        console.error("Erro na requisição:", erro);
        alert("Erro de conexão com o servidor");
      }
    });
  }

  window.logout = function () {
    localStorage.clear();
    window.location.href = "index.html";
  };

  const linkRecuperar = document.getElementById("link-recuperar-senha");
  if (linkRecuperar) {
    linkRecuperar.addEventListener("click", async (e) => {
      e.preventDefault();

      const usuarioInput = document.getElementById("usuario");
      const usuario = usuarioInput ? usuarioInput.value.trim() : "";

      if (!usuario) {
        alert("Por favor, preencha o campo de usuário antes de continuar.");
        return;
      }

      try {
        const resposta = await fetch("/api/enviar-codigo", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ usuario })
        });

        const resultado = await resposta.json();

        if (resposta.ok) {
          localStorage.setItem("username", usuario);
          localStorage.setItem("email", resultado.email);
          alert("Código enviado para o e-mail cadastrado.");
          window.location.href = "validar.html";
        } else {
          alert(resultado.erro || "Erro ao enviar código.");
        }
      } catch (erro) {
        console.error("Erro na requisição:", erro);
        alert("Erro de conexão com o servidor.");
      }
    });
  }

  const usuarioInput = document.getElementById("usuario");
  if (usuarioInput) {
    usuarioInput.addEventListener("blur", () => {
      const usuario = usuarioInput.value.trim();
      if (usuario) {
        localStorage.setItem("username", usuario);
      }
    });
  }
});

const isLocalhost = window.location.hostname === "127.0.0.1" || window.location.hostname === "localhost";


const API_BASE_URL = isLocalhost
  ? "http://127.0.0.1:5050"   
  : "";                       

document.getElementById("loginForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  const username = document.getElementById("username").value;
  const senha = document.getElementById("senha").value;

  try {
    const response = await fetch(`${API_BASE_URL}/api/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, senha })
    });

    if (!response.ok) {
      const text = await response.text();
      throw new Error(`Erro ${response.status}: ${text}`);
    }

    const data = await response.json();
    console.log("Login bem-sucedido:", data);
    alert(`Bem-vindo, ${data.usuario.username}!`);
  } catch (err) {
    console.error("Erro na requisição:", err);
    alert("Falha no login. Verifique suas credenciais.");
  }
});
