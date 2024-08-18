
    document.addEventListener('DOMContentLoaded', function() {
        const rows = document.querySelectorAll('tbody tr');
        rows.forEach((row, index) => {
            row.style.opacity = 0;
            setTimeout(() => {
                row.style.opacity = 1;
                row.style.transition = 'opacity 0.5s ease-in';
            }, index * 100);
        });
    });

