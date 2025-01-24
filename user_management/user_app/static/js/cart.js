function updateQuantity(cartId, change) {
    // AJAX request to update the quantity in the database
    console.log(`Updating quantity for Cart ID: ${cartId} with change: ${change}`);
    fetch(`/update_quantity/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken"), // Ensure the CSRF token is correct
        },
        body: JSON.stringify({
            cart_id: cartId,
            change: change,
        }),
    })
        .then((response) => response.json())
        .then((data) => {
            if (data.success) {
                location.reload(); // Reload to show updated quantity
            } else {
                console.error("Error:", data.error || "Failed to update quantity");
                alert("Failed to update quantity");
            }
        })
        .catch((error) => {
            console.error("Fetch error:", error);
            alert("Something went wrong");
        });
}



function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Check if this cookie starts with the name
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}



// **************************************************************************


    const addAddressBtn = document.getElementById("add-address-btn");
    const popupOverlay = document.getElementById("popup-overlay");
    const closePopupBtn = document.getElementById("close-popup-btn");

    // Show the popup
    addAddressBtn.addEventListener("click", () => {
        popupOverlay.style.display = "flex";
    });

    // Close the popup
    closePopupBtn.addEventListener("click", () => {
        popupOverlay.style.display = "none";
    });

