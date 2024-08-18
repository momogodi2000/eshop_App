document.addEventListener('DOMContentLoaded', function() {
    let cart = JSON.parse(localStorage.getItem('cartItems')) || [];
    const cartItems = document.getElementById('cart-items');
    const cartTotal = document.getElementById('cart-total');
    const checkoutBtn = document.getElementById('checkout-btn');
    const paymentModal = new bootstrap.Modal(document.getElementById('paymentModal'));
    const locationInfo = document.getElementById('location-info');
    const modalCartItems = document.getElementById('modal-cart-items');
    const modalCartTotal = document.getElementById('modal-cart-total');
    const confirmPaymentBtn = document.getElementById('confirm-payment');
    const phoneNumberInput = document.getElementById('phone-number'); // New phone number input

    document.querySelectorAll('.add-to-cart').forEach(button => {
        button.addEventListener('click', function() {
            const productId = this.dataset.id;
            const productName = this.dataset.name;
            const productPrice = parseFloat(this.dataset.price);

            const product = cart.find(p => p.id === productId);
            if (product) {
                product.quantity += 1;
            } else {
                cart.push({ id: productId, name: productName, price: productPrice, quantity: 1 });
            }

            updateCart();
        });
    });

    function updateCart() {
        cartItems.innerHTML = '';
        let total = 0;

        cart.forEach(product => {
            const item = document.createElement('li');
            item.className = 'list-group-item d-flex justify-content-between align-items-center';
            item.innerHTML = `${product.name} x ${product.quantity} <span>${(product.price * product.quantity).toFixed(2)} FCFA</span>`;
            cartItems.appendChild(item);

            total += product.price * product.quantity;
        });

        cartTotal.innerText = total.toFixed(2);
        localStorage.setItem('cartItems', JSON.stringify(cart));
        localStorage.setItem('cartTotal', total.toFixed(2));
    }

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
        modalCartItems.innerHTML = cart.map(item => `
            <li class="list-group-item d-flex justify-content-between align-items-center">
                ${item.name} x ${item.quantity}
                <span>${(item.price * item.quantity).toFixed(2)} FCFA</span>
            </li>
        `).join('');
        modalCartTotal.textContent = parseFloat(localStorage.getItem('cartTotal')).toFixed(2);

        paymentModal.show();
    });

    confirmPaymentBtn.addEventListener('click', () => {
        const paymentMethod = document.getElementById('payment-method').value;
        const phoneNumber = phoneNumberInput.value.trim(); // Get phone number from input

        if (!phoneNumber) {
            alert("Phone number is required for Campay payment.");
            return;
        }

        fetch('/process-payment/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                paymentMethod: paymentMethod === 'campay' ? 'campay' : paymentMethod,
                phoneNumber: phoneNumber,
                cartItems: cart,
                cartTotal: localStorage.getItem('cartTotal')
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Payment successful!');
                window.location.href = `/download-receipt/${data.receiptId}/`;
            } else {
                alert('Payment failed. Please try again.');
            }
        })
        .catch(error => {
            alert('An error occurred. Please try again later.');
            console.error('Payment error:', error);
        });
    });

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
