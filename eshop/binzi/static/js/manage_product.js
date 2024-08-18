/* scripts.js */

document.addEventListener('DOMContentLoaded', function () {
    // Example animation: Fade-in effect on page load
    const elements = document.querySelectorAll('.card, .table, form');
    elements.forEach((element) => {
        element.style.opacity = 0;
        element.style.transition = 'opacity 1s ease-in-out';
        element.style.opacity = 1;
    });

    // Example animation: Button click effect
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach((button) => {
        button.addEventListener('click', function () {
            this.classList.add('clicked');
        });
    });
});
