window.onload = function () {
  const passwordInput = document.getElementById("password");
  const strengthBar = document.querySelector(".strength-bar");
  const strengthText = document.querySelector(".strength-text");

  passwordInput.addEventListener("input", () => {
    const value = passwordInput.value;
    let score;

    const result = zxcvbn(value);
    score = result.score;

    strengthBar.className = "strength-bar"; // reset

    if (value.length === 0) {
      strengthText.innerHTML = "&nbsp;";
      return;
    }

    switch (result.score) {
      case 0:
      case 1:
        strengthBar.classList.add("weak");
        strengthText.textContent = "Senha fraca";
        break;

      case 2:
        strengthBar.classList.add("medium");
        strengthText.textContent = "Senha média";
        break;

      case 3:
        strengthBar.classList.add("strong");
        strengthText.textContent = "Senha forte";
        break;

      case 4:
        strengthBar.classList.add("very-strong");
        strengthText.textContent = "Senha muito forte";
        break;
    }
  });
};
