window.onload = function () {
  const toggle = document.getElementById("togglePassword");
  const password = document.getElementById("password");
  const icon = document.getElementById("icon");

  toggle.addEventListener("click", () => {
    const isPassword = password.type === "password";

    password.type = isPassword ? "text" : "password";
    icon.className = isPassword ? "fa fa-eye-low" : "fa fa-eye";
  });
};
