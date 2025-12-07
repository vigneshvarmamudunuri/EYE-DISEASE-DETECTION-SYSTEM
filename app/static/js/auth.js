// static/js/auth.js
const API_AUTH = "/auth";

function showMessage(form, type, text) {
  const msg = form.querySelector('.message');
  if (!msg) return;
  msg.className = 'message ' + (type || '');
  msg.textContent = text;
  msg.style.display = 'block';
  setTimeout(()=> { msg.style.display = 'none'; }, 5000);
}

document.addEventListener('DOMContentLoaded', () => {
  const regForm = document.getElementById('register-form');
  const loginForm = document.getElementById('login-form');

  if (regForm) {
    regForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const email = document.getElementById('reg-email').value.trim();
      const password = document.getElementById('reg-password').value.trim();
      try {
        const res = await fetch(API_AUTH + '/register', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email, password })
        });
        const data = await res.json();
        if (res.ok) {
          showMessage(regForm, 'success', 'Registration successful! Redirecting to login...');
          setTimeout(()=> location.href = '/login.html', 1600);
        } else {
          showMessage(regForm, 'error', data.detail || 'Registration failed');
        }
      } catch (err) {
        showMessage(regForm, 'error', 'Network error');
      }
    });
  }

  if (loginForm) {
    loginForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const email = document.getElementById('email').value.trim();
      const password = document.getElementById('password').value.trim();
      const params = new URLSearchParams();
      params.append('username', email);
      params.append('password', password);
      try {
        const res = await fetch(API_AUTH + '/token', {
          method: 'POST',
          headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
          body: params.toString()
        });
        const data = await res.json();
        if (res.ok) {
          localStorage.setItem('token', data.access_token);
          showMessage(loginForm, 'success', 'Login successful! Redirecting...');
          setTimeout(()=> location.href = '/dashboard.html', 900);
        } else {
          showMessage(loginForm, 'error', data.detail || 'Login failed');
        }
      } catch (err) {
        showMessage(loginForm, 'error', 'Network error');
      }
    });
  }
});
