document.addEventListener('DOMContentLoaded', function () {
    const teamMembers = document.querySelectorAll('.team-member');
    
    teamMembers.forEach(member => {
        member.addEventListener('mouseover', () => {
            member.style.transform = 'scale(1.05)';
            member.style.transition = 'transform 0.3s ease-in-out';
        });

        member.addEventListener('mouseout', () => {
            member.style.transform = 'scale(1)';
        });
    });
});

// JavaScript for any dynamic behavior or enhancements

document.addEventListener('DOMContentLoaded', function() {
    console.log('About Us page loaded.');
    // Add any custom JavaScript functionality here
});
