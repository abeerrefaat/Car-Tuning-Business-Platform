// Booking Checkout JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // Get elements
    const paymentButton = document.getElementById('make-payment');
    const bookingForm = document.getElementById('booking-form');
    const dateInput = document.getElementById('booking_date');
    const timeSelect = document.getElementById('booking_time');
    const notesInput = document.getElementById('notes');
    const serviceId = document.getElementById('service_id').value;
    
    // Function to validate the form
    function validateForm() {
        if (!dateInput.value) {
            alert('Please select a date');
            return false;
        }
        
        if (!timeSelect.value) {
            alert('Please select a time slot');
            return false;
        }
        
        return true;
    }
    
    // Handle payment button click
    if (paymentButton) {
        paymentButton.addEventListener('click', function(e) {
            e.preventDefault();
            
            if (!validateForm()) {
                return;
            }
            
            // Process the payment and booking
            processBooking();
        });
    }
    
    // Function to process the booking
    function processBooking() {
        // Get form data
        const bookingData = {
            booking_date: dateInput.value,
            booking_time: timeSelect.value,
            notes: notesInput.value
        };
        
        // Send data to server
        fetch(`/process_booking/${serviceId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getToken('csrftoken')
            },
            body: JSON.stringify({
                booking: bookingData
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Redirect to success page
                window.location.href = '/booksuccess/';
            } else {
                alert('Error: ' + data.error);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred. Please try again.');
        });
    }
    
    // Function to get CSRF token
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
    
    // Disable past dates in date picker
    if (dateInput) {
        // Get today's date
        const today = new Date();
        
        // Format today's date to YYYY-MM-DD
        const yyyy = today.getFullYear();
        const mm = String(today.getMonth() + 1).padStart(2, '0');
        const dd = String(today.getDate()).padStart(2, '0');
        const formattedDate = `${yyyy}-${mm}-${dd}`;
        
        // Set minimum date
        dateInput.min = formattedDate;
        
        // Validate date selection to exclude weekends
        dateInput.addEventListener('change', function() {
            const selectedDate = new Date(this.value);
            const day = selectedDate.getDay();
            
            // Check if weekend (0 = Sunday, 6 = Saturday)
            if (day === 0 || day === 6) {
                alert('Please select a weekday (Monday to Friday)');
                this.value = '';
            }
        });
    }
});
