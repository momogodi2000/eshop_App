// scripts.js

document.addEventListener("DOMContentLoaded", function () {
  // Auto-fill the date input with the current date
  const dateInput = document.querySelector('input[type="date"]');
  if (dateInput) {
      const today = new Date();
      const day = String(today.getDate()).padStart(2, '0');
      const month = String(today.getMonth() + 1).padStart(2, '0'); // January is 0!
      const year = today.getFullYear();
      
      // Format: YYYY-MM-DD
      dateInput.value = `${year}-${month}-${day}`;
  }
});



  $(document).ready(function() {
    $('button[type="submit"]').click(function() {
      $(this).closest('form').submit();
    });
  });



     // Geolocation: Get user's current location
     if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(function (position) {
          const latitude = position.coords.latitude;
          const longitude = position.coords.longitude;
          const location = `${latitude}, ${longitude}`;
          document.getElementById("location").value = location;
      }, function (error) {
          console.error("Error retrieving location:", error);
      });
  } else {
      console.error("Geolocation is not supported by this browser.");
  }

  // Star Rating System
  const starContainer = document.getElementById("star-rating");
  const stars = 5;
  let selectedRating = 0;

  // Create stars dynamically
  for (let i = 1; i <= stars; i++) {
      const star = document.createElement("span");
      star.classList.add("star");
      star.setAttribute("data-value", i);
      star.innerHTML = "&#9733;"; // Unicode for star
      starContainer.appendChild(star);

      // Handle hover effect
      star.addEventListener("mouseover", function () {
          highlightStars(i);
      });

      // Handle click event
      star.addEventListener("click", function () {
          selectedRating = i;
          document.getElementById("rating").value = selectedRating;
      });
  }

  // Remove highlight when mouse leaves the star container
  starContainer.addEventListener("mouseleave", function () {
      highlightStars(selectedRating);
  });

  // Highlight stars based on current selection
  function highlightStars(rating) {
      const stars = document.querySelectorAll("#star-rating .star");
      stars.forEach((star, index) => {
          if (index < rating) {
              star.classList.add("highlight");
          } else {
              star.classList.remove("highlight");
          }
      });
  }
