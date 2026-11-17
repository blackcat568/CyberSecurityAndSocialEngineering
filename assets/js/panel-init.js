(function() {
  const panel = document.getElementById('article-panel');
  const toggle = document.getElementById('panel-toggle');
  if (!panel || !toggle) return;

  // Определяем язык: сначала <html lang="...">, затем fallback по URL
  function detectLang() {
    const htmlLang = (document.documentElement.lang || '').toLowerCase();
    if (htmlLang.startsWith('ru')) return 'ru';
    if (htmlLang.startsWith('en')) return 'en';
    const path = window.location.pathname.toLowerCase();
    return path.includes('-rus') ? 'ru' : 'en';
  }

  const lang = detectLang();
  const labels = {
    ru: { open: '📚 Статьи',   close: '📚 Свернуть' },
    en: { open: '📚 Articles', close: '📚 Collapse' }
  };

  // Ставим стартовый текст кнопки (на случай, если в HTML стоит не тот)
  toggle.textContent = labels[lang].open;

  let isOpen = false;

  toggle.addEventListener('click', function() {
    isOpen = !isOpen;
    panel.style.left = isOpen ? '0px' : '-320px';
    toggle.textContent = isOpen ? labels[lang].close : labels[lang].open;
  });
})();
