(function () {
  const KEY = 'theme';
  const THEMES = ['light', 'dark', 'deuteranomaly'];

  function detectDefault() {
    try {
      if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
        return 'dark';
      }
    } catch (_) {}
    return 'light';
  }

  function applyTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    const label = theme === 'light' ? 'Claro'
                : theme === 'dark' ? 'Escuro'
                : 'Daltonismo (Deuteranomalia)';
    const buttons = document.querySelectorAll('[data-theme-toggle]');
    buttons.forEach((btn) => {
      btn.setAttribute('aria-label', 'Trocar tema (atual: ' + label + ')');
      btn.textContent = label;
    });
  }

  function loadTheme() {
    const saved = localStorage.getItem(KEY);
    return THEMES.includes(saved) ? saved : detectDefault();
  }

  function nextTheme(current) {
    const i = THEMES.indexOf(current);
    return THEMES[(i + 1) % THEMES.length];
  }

  let current = loadTheme();
  applyTheme(current);

  window.__toggleTheme = function () {
    current = nextTheme(current);
    localStorage.setItem(KEY, current);
    applyTheme(current);
  };
})();
