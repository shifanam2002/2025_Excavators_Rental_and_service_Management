function handleBookingClick(driverId) {
    // Check if the user is logged in by using Django's context variable
    const isLoggedIn = "{{ is_logged_in|yesno:'true,false' }}";
    if (isLoggedIn === "false") {
        alert("You need to sign in and have an active account to book a driver.");
    // Redirect to login page
        const currentUrl = window.location.href;
        window.location.href = `{% url 'login' %}?next=${encodeURIComponent(currentUrl)}`;
    } else {
    // Code to show booking modal if logged in and active
    openBookingModal(driverId);
    }
  }
  function openBookingModal(driverId) {
    // Hide the driver modal if it’s open
    $('#driverModal' + driverId).modal('hide');
    
    // Set the driver_id in the hidden field of the booking form
    document.getElementById("driver_id").value = driverId;

    // Display the booking modal
    document.getElementById("bookingModal").style.display = "block";
}


    // Close modal
    function closeModal() {
        document.getElementById("bookingModal").style.display = "none";
    }

    // Close modal when clicking outside
    window.onclick = function(event) {
        var modal = document.getElementById("bookingModal");
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }

    


// Function to close the status modal
function closeStatusModal() {
    document.getElementById("statusModal").style.display = "none";
}

// ******************************************************************************************

function validateStep(step) {
    const stepContainer = document.getElementById(`step-${step}`);
    const inputs = stepContainer.querySelectorAll("input, select, textarea");
    let valid = true;

    // Reset any previous error messages
    stepContainer.querySelectorAll('.error-message').forEach(el => el.remove());

    inputs.forEach(input => {
        if (!input.value) {
            valid = false;

            // Display an error message
            const error = document.createElement('div');
            error.classList.add('error-message');
            error.style.color = 'red';
            error.innerText = `${input.name} is required.`;
            input.parentNode.appendChild(error);
        }
    });

    return valid;
}

function nextStep(currentStep) {
    if (validateStep(currentStep)) {
        document.getElementById(`step-${currentStep}`).style.display = 'none';
        document.getElementById(`step-${currentStep + 1}`).style.display = 'block';
    }
}
    function prevStep(currentStep) {
        const current = document.getElementById(`step-${currentStep}`);
        const previous = document.getElementById(`step-${currentStep - 1}`);
        current.style.display = 'none';
        previous.style.display = 'block';
    }

document.getElementById('id_payment_mode').addEventListener('change', function() {
const paymentAmountSection = document.getElementById('payment-amount-section');
if (this.value === 'Hourly' || this.value === 'Per Day') {
    paymentAmountSection.style.display = 'block';
} else {
    paymentAmountSection.style.display = 'none';
}
});

// ******************************************************************************


document.getElementById('hero-section').addEventListener('click', function() {
  document.getElementById('hero-title').classList.toggle('animate-title');
  document.getElementById('hero-subtitle').classList.toggle('animate-subtitle');
  document.getElementById('hero-btn').classList.toggle('animate-btn');
});


// ******************************************************************************************************************

function closeModals() {
    history.back(); // Navigates to the previous page
}

function toggleEnquiry(button){
    if(button.textContent == 'Enquire'){
        button.textContent == 'Enquired'
        button.style.backgroundColor = 'green'
    }
    else{
        button.textContent == 'Enquire'
        button.style.backgroundColor = "";
    }
}



function openContactForm(spareId) {
    document.getElementById('contactForm').style.display = 'block';
    document.getElementById('spareIdInput').value = spareId;
}

function closeContactForm() {
    document.getElementById('contactForm').style.display = 'none';
}






    
