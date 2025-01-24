const modal = document.getElementById('myModal');
const modalContent = document.querySelector('.modal-content');

window.onclick = function(event) {
  if (event.target === modal) {
    // Prevent modal close
    console.log('Click outside prevented');
  }
};

// **********************************************************************

function playVideoAfterDelay() {
  const video = document.getElementById('safetyVideo');
  setTimeout(() => {
      video.play();
  }, 600); // Delay in milliseconds (5000ms = 5 seconds)
}

// Call the function when the page loads
window.onload = playVideoAfterDelay;

// ************************************************************************************


    // Function to toggle the visibility of forms
    function showForm(formId) {
      // Hide all forms
      document.getElementById('exca_form').style.display = 'none';
      document.getElementById('category_form').style.display = 'none';

      // Show the selected form
      document.getElementById(formId).style.display = 'block';
  }

  // *******************************************************************************

  document.getElementById('hero-section').addEventListener('click', function() {
    document.getElementById('hero-title').classList.toggle('animate-title');
    document.getElementById('hero-subtitle').classList.toggle('animate-subtitle');
    document.getElementById('hero-btn').classList.toggle('animate-btn');
  });



  function goBack() {
    window.history.back(); // Redirects to the previous page in the browser history
}



function handlePayment() {
  const selectedPaymentMethod = document.querySelector('input[name="payment_method"]:checked');
  const totalAmount = document.querySelector('input[name="total_amount"]').value;
  const cartItemIds = document.querySelector('input[name="cart_item_ids"]').value;

  if (!selectedPaymentMethod) {
      alert("Please select a payment method.");
      return;
  }

  const paymentMethod = selectedPaymentMethod.value;

  const baseUrls = {
      // credit_card: "/payments/payment/",
      gpay: "/payments/gpay_payment/",
      cash_on_delivery: "/payments/cash_on_delivery/"
  };

  if (baseUrls[paymentMethod]) {
      window.location.href = `${baseUrls[paymentMethod]}?total_amount=${totalAmount}&cart_item_ids=${cartItemIds}`;
  } else {
      alert("Invalid payment method selected.");
  }
}