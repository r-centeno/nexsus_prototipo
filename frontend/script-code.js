document.addEventListener("DOMContentLoaded", () => {
  const usuario = localStorage.getItem("usuario");
  document.getElementById("usuario").value = usuario || "";

  const inputs = document.querySelectorAll(".code");
  const confirmButton = document.getElementById("confirmButton");

  inputs.forEach((input, index) => {
    input.addEventListener("input", () => {
      if (input.value.length === 1 && index < inputs.length - 1) {
        inputs[index + 1].focus();
      }
      checkInputs();
    });

    input.addEventListener("keydown", (e) => {
      if (e.key === "Backspace" && input.value === "" && index > 0) {
        inputs[index - 1].focus();
      }
    });
  });

  function checkInputs() {
    const allFilled = Array.from(inputs).every(input => input.value.length === 1);
    confirmButton.disabled = !allFilled;
  }

  document.getElementById("codeForm").addEventListener("submit", async (e) => {
    e.preventDefault();

    const codigo = Array.from(inputs).map(input => input.value).join("");
    const email = localStorage.getItem("email");
    if (codigo.length !== 6 || !email) {
      alert("Código inválido ou usuário não identificado.");
      return;
    }

    try {
      const resposta = await fetch("/api/validar-codigo", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ email, codigo })
      });

      const resultado = await resposta.json();

      if (resposta.ok) {
        alert("Código validado com sucesso.");
        window.location.href = "reset.html";
      } else {
        alert(resultado.erro || "Código inválido.");
      }
    } catch (erro) {
      console.error("Erro na requisição:", erro);
      alert("Erro de conexão com o servidor.");
    }
  });
});
