/* MotoTaller — JS utilities */

// ── Toast notifications ────────────────────────────────────────────────────────
function showToast(message, type = 'info', duration = 4000) {
  let container = document.getElementById('toast-container');
  if (!container) {
    container = document.createElement('div');
    container.id = 'toast-container';
    document.body.appendChild(container);
  }
  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  toast.textContent = message;
  container.appendChild(toast);
  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateY(10px)';
    toast.style.transition = 'opacity .3s, transform .3s';
    setTimeout(() => toast.remove(), 300);
  }, duration);
}

// Auto-dismiss Django messages as toasts
document.addEventListener('DOMContentLoaded', function () {
  document.querySelectorAll('[data-message]').forEach(el => {
    const type = el.dataset.type || 'info';
    showToast(el.dataset.message, type);
    el.remove();
  });
});

// ── Confirmación de acciones peligrosas ───────────────────────────────────────
document.addEventListener('click', function (e) {
  const btn = e.target.closest('[data-confirm]');
  if (!btn) return;
  if (!confirm(btn.dataset.confirm)) e.preventDefault();
});

// ── Formato de peso chileno ───────────────────────────────────────────────────
function formatPesos(n) {
  return '$' + Math.round(n).toLocaleString('es-CL');
}

// ── Sidebar: active link ──────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', function () {
  const path = window.location.pathname;
  document.querySelectorAll('.nav-item').forEach(a => {
    const href = a.getAttribute('href');
    if (href && href !== '/' && path.startsWith(href)) {
      a.classList.add('bg-gray-800', 'text-white');
      a.classList.remove('text-gray-300');
    }
  });
});
