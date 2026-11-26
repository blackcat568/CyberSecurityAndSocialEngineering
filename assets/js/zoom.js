// assets/js/zoom.js
(function () {
  // Закрыть все увеличенные картинки, кроме указанной (или все, если не указана)
  function closeZoomed(except) {
    document.querySelectorAll('img.zoomed').forEach(function (img) {
      if (img !== except) img.classList.remove('zoomed');
    });
  }

  // Клик по картинке с атрибутом data-zoom
  document.addEventListener('click', function (e) {
    var img = e.target.closest('img[data-zoom]');
    if (img) {
      // Сначала закрываем все остальные, потом переключаем текущую
      closeZoomed(img);
      img.classList.toggle('zoomed');
      return;
    }

    // Клик вне увеличенной картинки — закрываем все
    if (e.target.classList.contains('zoomed')) {
      // клик по самой картинке (она fixed, может быть вне потока)
      e.target.classList.remove('zoomed');
      return;
    }

    // Клик по фону (вне картинки) — закрываем все увеличенные
    closeZoomed(null);
  });

  // Esc — закрыть все
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') closeZoomed(null);
  });
})();
