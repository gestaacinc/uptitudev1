document.addEventListener("DOMContentLoaded", () => {
  // Elements
  const modal = document.getElementById("forgot-password-modal");
  const forgotPasswordLink = document.getElementById("forgot-password-link");
  const closeModal = document.getElementById("close-modal");
  const forgotPasswordForm = modal?.querySelector("form");
  const flashMessages = document.querySelectorAll(".flash-message");

  /**
   * Show the Forgot Password modal.
   */
  const showModal = () => {
    if (modal) {
      modal.classList.remove("hidden");
      modal.setAttribute("aria-hidden", "false");
    }
  };

  /**
   * Hide the Forgot Password modal.
   */
  const hideModal = () => {
    if (modal) {
      modal.classList.add("hidden");
      modal.setAttribute("aria-hidden", "true");
    }
  };

  /**
   * Event listener to handle clicking outside the modal.
   */
  const handleOutsideClick = (event) => {
    if (event.target === modal) {
      hideModal();
    }
  };

  /**
   * Auto-hide flash messages after a delay.
   */
  const autoHideFlashMessages = () => {
    if (flashMessages.length > 0) {
      setTimeout(() => {
        flashMessages.forEach((message) => {
          message.style.transition = "opacity 0.5s";
          message.style.opacity = "0";
          setTimeout(() => {
            message.remove();
          }, 500); // Wait for fade-out transition
        });
      }, 3000); // 3-second delay before fade-out starts
    }
  };

  /**
   * Handle Forgot Password form submission with AJAX.
   */
  const handleForgotPasswordSubmit = async (event) => {
    event.preventDefault();

    const emailInput = document.getElementById("forgot-email");
    const email = emailInput?.value;

    if (!email) {
      alert("Please enter a valid email.");
      return;
    }

    try {
      // Display a loading spinner (optional, add your UI spinner implementation here)
      forgotPasswordForm.querySelector("button[type='submit']").textContent =
        "Sending...";

      const response = await fetch(forgotPasswordForm.action, {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: new URLSearchParams({ email }),
      });

      const result = await response.json();

      if (response.ok) {
        alert(result.message); // Success message
        hideModal(); // Close the modal
      } else {
        alert(result.message); // Error message
      }
    } catch (error) {
      console.error("Error submitting forgot password form:", error);
      alert("An error occurred. Please try again later.");
    } finally {
      // Reset button text
      forgotPasswordForm.querySelector("button[type='submit']").textContent =
        "Send Reset Link";
    }
  };

  // Attach event listeners
  if (forgotPasswordLink) {
    forgotPasswordLink.addEventListener("click", (event) => {
      event.preventDefault();
      showModal();
    });
  }

  if (closeModal) {
    closeModal.addEventListener("click", hideModal);
  }

  if (modal) {
    window.addEventListener("click", handleOutsideClick);
  }

  if (forgotPasswordForm) {
    forgotPasswordForm.addEventListener("submit", handleForgotPasswordSubmit);
  }

  // Initialize flash messages auto-hide
  autoHideFlashMessages();
});
