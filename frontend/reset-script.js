document.getElementById("resetForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  const senha = document.getElementById("password").value.trim();
  const confirmar = document.getElementById("confirmPassword").value.trim();
  const email = localStorage.getItem("email");

  if (!senha || !confirmar || senha !== confirmar) {
    alert("As senhas não conferem.");
    return;
  }

  try {
    const resposta = await fetch("/api/redefinir-senha", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ email, novaSenha: senha })
    });

    const resultado = await resposta.json();

    if (resposta.ok) {
      alert("Senha redefinida com sucesso.");
      window.location.href = "index.html";
    } else {
      alert(resultado.erro || "Erro ao redefinir senha.");
    }
  } catch (erro) {
    console.error("Erro na requisição:", erro);
    alert("Erro de conexão com o servidor.");
  }
});
