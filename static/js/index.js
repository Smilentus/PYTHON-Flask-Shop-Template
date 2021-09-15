// Первый слайдер
const carouselSlide = document.querySelector('.slider-main-slide');
const carouselImages = document.querySelectorAll('.slider-main-slide .slider-block');

const sliderLeftBtn = document.querySelector("#sliderLeft");
const sliderRightBtn = document.querySelector("#sliderRight");

let counter = 1;
let size = carouselImages[0].clientWidth;

carouselSlide.style.transform = 'translateX(' + (-size * counter) + 'px)';
 
sliderRightBtn.addEventListener('click', ()=>{
    if (counter >= carouselImages.length - 1) return;
    carouselSlide.style.transition = "transform 0.4s ease-in-out";
    counter++;
    carouselSlide.style.transform = 'translateX(' + (-size * counter) + "px)";
});

sliderLeftBtn.addEventListener('click', ()=>{
    if (counter <= 0) return;
    carouselSlide.style.transition = "transform 0.4s ease-in-out";
    counter--;
    carouselSlide.style.transform = 'translateX(' + (-size * counter) + "px)";
});

carouselSlide.addEventListener('transitionend', ()=>{
    if (carouselImages[counter].id === 'lastClone')
    {
        carouselSlide.style.transition = "none";
        counter = carouselImages.length - 2;
        carouselSlide.style.transform = 'translateX(' + (-size * counter) + "px)";
    }
    if (carouselImages[counter].id === 'firstClone')
    {
        carouselSlide.style.transition = "none";
        counter = carouselImages.length - counter;
        carouselSlide.style.transform = 'translateX(' + (-size * counter) + "px)";
    }
});

window.addEventListener('resize', ()=>{
    size = carouselImages[0].clientWidth;

    carouselSlide.style.transition = "none";
    carouselSlide.style.transform = 'translateX(' + (-size * counter) + "px)";
})