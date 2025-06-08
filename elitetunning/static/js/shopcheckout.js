// Wait for DOM to be fully loaded before executing
document.addEventListener('DOMContentLoaded', function() {
    console.log("User status:", user, typeof user);

    let isSubmitting = false;

    // Redirect to login if user is not authenticated
    if (typeof user === 'undefined' || user === 'AnonymousUser') {
        console.log("User is not logged in, redirecting to login");
        window.location.href = "/login/";
        return; // Stop execution of the rest of the script
    }

    // Get the total from the DOM
    const totalElement = document.getElementById('total-price');
    if (!totalElement) {
        console.error("Total price element not found!");
        window.location.href = "/cart/";
        return; // Stop execution if no total price element is found
    }
    
    var total = totalElement.innerText.replace('$', '');
    console.log('Cart total:', total);

    // Get all required elements
    const continueBtn = document.getElementById('continue-btn');
    const paymentInfo = document.getElementById('payment-info');
    const makePaymentBtn = document.getElementById('make-payment');
    const backLink = document.getElementById('back-link');

    // Debug: Check if elements exist
    console.log("Continue button:", continueBtn);
    console.log("Payment info:", paymentInfo);
    console.log("Make payment button:", makePaymentBtn);
    console.log("Back link:", backLink);

    // Handle form submission
    if (continueBtn && paymentInfo) {
        continueBtn.addEventListener('click', function(e) {
            e.preventDefault();
            console.log('Continue button clicked');
            
            if (validateForm()) {
                console.log('Form validated successfully');
                // Hide form buttons and show payment
                continueBtn.classList.add("hidden");
                if (backLink) backLink.classList.add("hidden");
                paymentInfo.classList.remove("hidden");
                
                // Scroll to payment for better UX
                paymentInfo.scrollIntoView({ behavior: 'smooth' });
            }
        });
    }

    // Handle payment button
    if (makePaymentBtn) {
        makePaymentBtn.addEventListener('click', function(e) {
            e.preventDefault();
            console.log('Payment button clicked');
            
            // Prevent multiple submissions
            if (isSubmitting) {
                console.log('Form already being submitted');
                return;
            }
            
            // Set flag to indicate submission in progress
            isSubmitting = true;
            
            // Disable the button and show processing state
            makePaymentBtn.disabled = true;
            makePaymentBtn.textContent = 'Processing...';
            
            submitFormData();
        });
    }

    function validateForm() {
        console.log('Validating form...');
        
        // Check all required fields
        const address = document.getElementById('address')?.value;
        const city = document.getElementById('city')?.value;
        const state = document.getElementById('state')?.value;
        
        if (!address || !city || !state) {
            alert('Please fill in all shipping information');
            return false;
        }
        
        return true;
    }

    function submitFormData() {
        console.log('Processing payment...');
    
        // Get the total from the DOM
        var total = document.getElementById('total-price').innerText.replace('$', '').trim();
        console.log('Total from page:', total);
    
        var userFormData = {
            'total': total
        };
        
        // Make sure to get the values correctly
        var shippingInfo = {
            'address': document.getElementById('address').value,
            'city': document.getElementById('city').value,
            'state': document.getElementById('state').value
        };
    
        // Log shipping info to verify it's correct
        console.log('Shipping Info to be sent:', shippingInfo);
    
        // Get CSRF token
        function getToken(name) {
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
        const csrftoken = getToken('csrftoken');
    
        // Construct the data to send
        const sendData = {
            'form': userFormData,
            'shipping': shippingInfo
        };
        console.log('Data being sent to server:', JSON.stringify(sendData));
    
        var url = "/process_order/";
        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            }, 
            body: JSON.stringify(sendData),
        })
        .then((response) => {
            if (!response.ok) {
                throw new Error('Server error: ' + response.status);
            }
            return response.json();
        })
        .then((data) => {
            console.log('Success response:', data);
            alert('Transaction completed');  
            window.location.href = "/shopsuccess/";
        })
        .catch((error) => {
            console.error('Error:', error);
            alert('Error processing order: ' + error.message);

            // Reset submission state on error
            isSubmitting = false;
            if (makePaymentBtn) {
                makePaymentBtn.disabled = false;
                makePaymentBtn.textContent = 'Pay with PayPal';
            }
        });
    }
});

