// Add animations or interactive features

// Example: Fade in animation for carousel captions
$('.carousel').on('slide.bs.carousel', function () {
    $('.carousel-caption').fadeOut(500);
});

$('.carousel').on('slid.bs.carousel', function () {
    $('.carousel-caption').fadeIn(500);
});


$(document).ready(function () {
    // Initialize tooltips
    $('[data-toggle="tooltip"]').tooltip();
    
    // Activate Bootstrap's tab functionality
    $('#product-tabs a:first').tab('show');
});