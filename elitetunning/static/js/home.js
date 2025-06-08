
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});


document.addEventListener('DOMContentLoaded', function() {
    // Set the explore section to visible immediately if needed
    const exploreSection = document.querySelector('.explore-section');
    if (!exploreSection) return;
    
    // Initial check if already in viewport
    checkVisibility();
    
    // Check on scroll
    window.addEventListener('scroll', checkVisibility);
    
    function checkVisibility() {
        const sectionPosition = exploreSection.getBoundingClientRect().top;
        const screenPosition = window.innerHeight / 1.3;
        
        if (sectionPosition < screenPosition) {
            exploreSection.classList.add('visible');
        }
    }
});