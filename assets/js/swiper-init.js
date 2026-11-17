// assets/js/swiper-init.js
const swiper = new Swiper('.swiper', {
    loop: true,
    centeredSlides: true,
    spaceBetween: 20,
    grabCursor: true,
    keyboard: true,
    navigation: {
        nextEl: '.swiper-button-next',
        prevEl: '.swiper-button-prev'
    },
    pagination: {
        el: '.swiper-pagination',
        clickable: true
    }
});
