document.addEventListener('DOMContentLoaded', () => {
    const checkoutBtn = document.getElementById('checkout-btn');
    const paymentModal = new bootstrap.Modal(document.getElementById('paymentModal'));
    const locationInfo = document.getElementById('location-info');
    const modalCartItems = document.getElementById('modal-cart-items');
    const modalCartTotal = document.getElementById('modal-cart-total');
    const paypalButtonContainer = document.getElementById('paypal-button-container');
    const confirmPaymentBtn = document.getElementById('confirm-payment');

    checkoutBtn.addEventListener('click', () => {
        // Fetch location
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(position => {
                const { latitude, longitude } = position.coords;
                locationInfo.textContent = `Latitude: ${latitude}, Longitude: ${longitude}`;
            }, error => {
                locationInfo.textContent = 'Unable to retrieve location.';
            });
        } else {
            locationInfo.textContent = 'Geolocation is not supported by this browser.';
        }

        // Populate cart details in the modal
        const cartItems = JSON.parse(localStorage.getItem('cartItems')) || [];
        const cartTotal = parseFloat(localStorage.getItem('cartTotal')) || 0;
        modalCartItems.innerHTML = cartItems.map(item => `
            <li class="list-group-item d-flex justify-content-between align-items-center">
                ${item.name}
                <span class="badge bg-primary rounded-pill">${item.price} FCFA</span>
            </li>
        `).join('');
        modalCartTotal.textContent = cartTotal.toFixed(2);

        // Initialize PayPal Button
        paypal.Buttons({
            createOrder: function(data, actions) {
                return actions.order.create({
                    purchase_units: [{
                        amount: {
                            currency_code: "USD",
                            value: (cartTotal / 600).toFixed(2) // Convert FCFA to USD
                        }
                    }]
                });
            },
            onApprove: function(data, actions) {
                return actions.order.capture().then(function(details) {
                    // Handle successful payment here
                    alert('Payment Successful!');
                    // Optionally send payment data to the backend
                    fetch('/process-payment/', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRFToken': getCookie('csrftoken')
                        },
                        body: JSON.stringify({
                            paymentMethod: 'paypal',
                            cartItems: cartItems,
                            cartTotal: cartTotal
                        })
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            // Redirect to download receipt
                            window.location.href = `/download-receipt/${data.receiptId}/`;
                        } else {
                            alert('Payment failed. Please try again.');
                        }
                    });
                });
            }
        }).render('#paypal-button-container');

        // Show the modal
        paymentModal.show();
    });

    confirmPaymentBtn.addEventListener('click', () => {
        const paymentMethod = document.getElementById('payment-method').value;
        const cartItems = JSON.parse(localStorage.getItem('cartItems')) || [];
        const cartTotal = parseFloat(localStorage.getItem('cartTotal')) || 0;

        if (paymentMethod === 'paypal') {
            // PayPal button will handle payment
            return;
        }

        // Handle other payment methods (e.g., Mobile Payment, Bank Payment)
        fetch('/process-payment/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                paymentMethod,
                cartItems,
                cartTotal
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Handle successful payment
                alert('Payment successful!');
                window.location.href = `/download-receipt/${data.receiptId}/`; // Redirect to download receipt
            } else {
                alert('Payment failed. Please try again.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred. Please try again.');
        });
    });
});
