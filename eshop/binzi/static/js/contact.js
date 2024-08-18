document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('form');
    if (form) {
        form.addEventListener('submit', (event) => {
            event.preventDefault();
            alert('Message sent successfully!');
            form.reset();
        });
    }
});

// JavaScript for Contact Us page interactions and animations

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('contactForm');
    const submitButton = document.getElementById('submitButton');
    
    // Add smooth scroll effect on submit
    form.addEventListener('submit', function(event) {
        event.preventDefault();
        submitButton.textContent = 'Sending...';
        
        // Simulate form submission process
        setTimeout(() => {
            // Reset button text and show success message (for demo purposes)
            submitButton.textContent = 'Send Message';
            form.reset();
            alert('Your message has been sent successfully!');
        }, 2000);
    });
});
