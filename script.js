function showTab(tabName) {
    const tabs = document.querySelectorAll('.tab');
    tabs.forEach(tab => tab.classList.remove('active'));
    const targetTab = document.getElementById(tabName);
    if (targetTab) {
        targetTab.classList.add('active');
        targetTab.scrollIntoView({
            behavior: 'smooth'
        });
    }
}

function handleUrlChange() {
    const path = window.location.pathname;
    let tabToShow = 'services'; // default tab

    if (path === '/about') {
        tabToShow = 'about';
    } else if (path === '/contact') {
        tabToShow = 'contact';
    }

    showTab(tabToShow);
}

document.addEventListener('DOMContentLoaded', function() {
    const header = document.querySelector('header');
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
    });

    const navLinks = document.querySelectorAll('nav a');
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href').substring(1);
            const url = '/' + (targetId === 'services' ? '' : targetId);
            history.pushState(null, '', url);
            showTab(targetId);
        });
    });

    // Handle the initial page load
    handleUrlChange();

    // Handle browser back/forward navigation
    window.addEventListener('popstate', handleUrlChange);
});