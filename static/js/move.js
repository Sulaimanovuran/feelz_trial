// Получаем все строки таблицы с классом lesson-row
const lessonRows = document.querySelectorAll('.lesson-row');

// Добавляем обработчик события клика к каждой строке
lessonRows.forEach(row => {
    row.addEventListener('click', () => {
        // Получаем ID урока из атрибута data-lesson-id
        const lessonId = row.dataset.lessonId;
        const leadId = row.dataset.leadId;
        // Теперь вы можете использовать этот ID для выполнения необходимых действий, например, перехода к странице урока
        window.location.href = `/lesson/move/${lessonId}/${leadId}`; // Пример URL для перехода к странице урока с определенным ID
    });
})


