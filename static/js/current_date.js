
// const currentDate = new Date();
// const formattedDate = currentDate.toISOString().split('T')[0];

document.addEventListener('DOMContentLoaded', function() {
    const currentDate = new Date();
    currentDate.setDate(8); // Set the desired default date (can be adjusted)
    currentDate.setMonth(1); // 0 for January, 1 for February etc.
    const formattedDate = currentDate.toISOString().split('T')[0];

    const todayElement = document.querySelector(`[data-date="${formattedDate}"]`);

    if (todayElement) {
        const offsetTop = todayElement.offsetTop;
        const container = document.querySelector('.container');
        container.scrollTo({
            top: offsetTop,
            behavior: 'smooth'
        });
    }
});
