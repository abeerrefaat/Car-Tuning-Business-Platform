document.querySelectorAll('.question').forEach(question => {
    question.addEventListener('click', () => {
        question.nextElementSibling.classList.toggle('active');
        question.querySelector('span').textContent = 
            question.nextElementSibling.classList.contains('active') ? '-' : '+';
    });
});