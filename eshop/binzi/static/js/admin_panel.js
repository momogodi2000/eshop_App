document.addEventListener('DOMContentLoaded', function () {
    const menuToggle = document.querySelector('.menu-toggle');
    const dashboardNav = document.querySelector('.dashboard-nav');
    const dashboardApp = document.querySelector('.dashboard-app');

    menuToggle.addEventListener('click', function () {
        if (dashboardNav.classList.contains('closed')) {
            dashboardNav.classList.remove('closed');
            dashboardApp.classList.add('shifted');
        } else {
            dashboardNav.classList.add('closed');
            dashboardApp.classList.remove('shifted');
        }
    });

    // Optional: Add event listener for clicks outside the sidebar to close it
    document.addEventListener('click', function (event) {
        if (!dashboardNav.contains(event.target) && !menuToggle.contains(event.target)) {
            dashboardNav.classList.add('closed');
            dashboardApp.classList.remove('shifted');
        }
    });
});
