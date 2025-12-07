const API_BASE = "http://127.0.0.1:8000/auth";

// Utility function to show message
function showMessage(element, type, text) {
  const msgBox = element.querySelector(".message");
  msgBox.className = `message ${type}`;
  msgBox.textContent = text;
  msgBox.style.display = "block";
  setTimeout(() => {
    msgBox.style.display = "none";
  }, 4000); // hides after 4s
}

document.addEventListener("DOMContentLoaded", () => {
  const regForm = document.getElementById("register-form");
  const loginForm = document.getElementById("login-form");

  if (regForm) {
    regForm.insertAdjacentHTML("afterbegin", '<div class="message"></div>');
    regForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const email = document.getElementById("reg-email").value.trim();
      const password = document.getElementById("reg-password").value.trim();

      const res = await fetch(`${API_BASE}/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });

      const data = await res.json();

      if (res.ok) {
        showMessage(regForm, "success", "✅ Registration successful! Redirecting to login...");
        setTimeout(() => (window.location.href = "login.html"), 2500);
      } else {
        showMessage(regForm, "error", data.detail || "Registration failed!");
      }
    });
  }

  if (loginForm) {
    loginForm.insertAdjacentHTML("afterbegin", '<div class="message"></div>');
    loginForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const email = document.getElementById("email").value.trim();
      const password = document.getElementById("password").value.trim();

      const body = new URLSearchParams();
      body.append("username", email);
      body.append("password", password);

      const res = await fetch(`${API_BASE}/token`, {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body,
      });

      const data = await res.json();

      if (res.ok) {
        localStorage.setItem("token", data.access_token);
        showMessage(loginForm, "success", "✅ Login successful! Redirecting...");
        setTimeout(() => (window.location.href = "index.html"), 2000);
      } else {
        showMessage(loginForm, "error", data.detail || "Invalid credentials!");
      }
    });
  }
});
