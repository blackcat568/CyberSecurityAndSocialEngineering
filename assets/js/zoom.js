// assets/js/zoom.js
(function () {
  // Автоматически переводим старые картинки с onclick на единый механизм
  document.querySelectorAll('img[onclick*="zoomed"]').forEach(function (img) {
    img.removeAttribute('onclick');
    img.setAttribute('data-zoom', '');
  });

  function closeZoomed(except) {
    document.querySelectorAll('img.zoomed').forEach(function (img) {
      if (img !== except) img.classList.remove('zoomed');
    });
  }

  document.addEventListener('click', function (e) {
    var img = e.target.closest('img[data-zoom]');
    if (img) {
      closeZoomed(img);
      img.classList.toggle('zoomed');
      return;
    }

    closeZoomed(null);
  });

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') closeZoomed(null);
  });
})();
