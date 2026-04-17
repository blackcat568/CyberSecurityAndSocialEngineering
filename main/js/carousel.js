(function() {
  const container = document.querySelector('.carousel-container');
  if (!container) return;
  const slidesContainer = container.querySelector('.carousel-slides');
  const slides = container.querySelectorAll('.carousel-slide');
  const prevBtn = container.querySelector('.carousel-prev');
  const nextBtn = container.querySelector('.carousel-next');
  const dotsContainer = container.querySelector('.carousel-dots');
  let currentIndex = 0;
  let autoTimer = null;

  function updateHeight() {
    const activeSlide = slides[currentIndex];
    const caption = activeSlide.querySelector('.carousel-caption');
    if (caption) {
      container.style.height = 'auto';
      const newHeight = caption.scrollHeight + 200;
      container.style.height = newHeight + 'px';
    }
  }

  function updateCarousel() {
    slidesContainer.style.transform = 'translateX(-' + (currentIndex * 100) + '%)';
    updateHeight();
    const dots = dotsContainer.querySelectorAll('.dot');
    dots.forEach((dot, idx) => {
      dot.classList.toggle('active', idx === currentIndex);
    });
  }

  function goToSlide(index) {
    if (index < 0) index = slides.length - 1;
    if (index >= slides.length) index = 0;
    currentIndex = index;
    updateCarousel();
  }

  for (let i = 0; i < slides.length; i++) {
    const dot = document.createElement('div');
    dot.classList.add('dot');
    dot.addEventListener('click', (function(idx) { return function() { goToSlide(idx); }; })(i));
    dotsContainer.appendChild(dot);
  }

  prevBtn.addEventListener('click', () => goToSlide(currentIndex - 1));
  nextBtn.addEventListener('click', () => goToSlide(currentIndex + 1));
  autoTimer = setInterval(() => goToSlide(currentIndex + 1), 10000);
  container.addEventListener('mouseenter', () => { if (autoTimer) clearInterval(autoTimer); });
  container.addEventListener('mouseleave', () => { autoTimer = setInterval(() => goToSlide(currentIndex + 1), 10000); });
  updateCarousel();
  window.addEventListener('resize', updateHeight);
})();
