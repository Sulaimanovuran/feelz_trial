const container = document.querySelector('.container');
const arrowLeft = document.querySelector('.arrow-left');
const arrowRight = document.querySelector('.arrow-right');

// Функция для прокрутки влево
function scrollLeft() {
    container.scrollBy({
        left: -500, // Настройте шаг прокрутки
        behavior: 'smooth'
    });
}

// Функция для прокрутки вправо
function scrollRight() {
    container.scrollBy({
        left: 500, // Настройте шаг прокрутки
        behavior: 'smooth'
    });
}

arrowLeft.addEventListener('click', scrollLeft);
arrowRight.addEventListener('click', scrollRight);




