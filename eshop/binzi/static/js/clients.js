// Toggle dashboard nav on mobile devices
const dashboardNav = document.querySelector('.dashboard-nav');
const menuToggle = document.querySelector('.menu-toggle');

menuToggle.addEventListener('click', () => {
  dashboardNav.classList.toggle('show');
});

// Initialize catalog tabs
const catalogTabs = document.querySelector('.catalog-tabs');
const catalogTabsLinks = catalogTabs.querySelectorAll('.nav-link');

catalogTabsLinks.forEach((link) => {
  link.addEventListener('click', (e) => {
    e.preventDefault();
    const tabId = link.getAttribute('href');
    const tabContent = document.querySelector(tabId);
    tabContent.classList.add('active');
    link.classList.add('active');
  });
});