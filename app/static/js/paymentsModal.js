document.addEventListener("DOMContentLoaded", () => {
  const openPaymentsModal = () => {
    const modal = document.getElementById("paymentsModal");
    const spinner = modal.querySelector(".loader");
    const table = modal.querySelector("table");
    const tbody = modal.querySelector("tbody");

    // Reset modal content
    spinner.style.display = "flex";
    table.style.display = "none";
    tbody.innerHTML = "";

    // Fetch data from the backend
    fetch("/admin/pending_payments")
      .then((response) => response.json())
      .then((data) => {
        // Populate the table with fetched data
        data.forEach((item) => {
          const row = document.createElement("tr");

          row.className = "hover:bg-gray-50"; // TailwindCSS class for hover effect

          // Enrollee Name Cell
          const enrolleeCell = document.createElement("td");
          enrolleeCell.className = "border px-4 py-2 text-gray-800";
          enrolleeCell.textContent = item.enrollee_name; // Correct field
          row.appendChild(enrolleeCell);

          // Course Name Cell
          const courseCell = document.createElement("td");
          courseCell.className = "border px-4 py-2 text-gray-800";
          courseCell.textContent = item.course_name; // Correct field
          row.appendChild(courseCell);

          // Pending Balance Cell
          const balanceCell = document.createElement("td");
          balanceCell.className = "border px-4 py-2 text-gray-800 text-right";
          balanceCell.textContent = item.pending_balance; // Correct field
          row.appendChild(balanceCell);

          // Append the row to the table body
          tbody.appendChild(row);
        });

        // Hide spinner and show table
        spinner.style.display = "none";
        table.style.display = "table";
      })
      .catch((error) => {
        console.error("Error fetching payments data:", error);
        // Optionally show an error message in the table
        const errorRow = document.createElement("tr");
        const errorCell = document.createElement("td");
        errorCell.colSpan = 3; // Adjust the colspan based on the number of columns
        errorCell.className = "text-red-500 text-center px-4 py-2";
        errorCell.textContent = "An error occurred while fetching data.";
        errorRow.appendChild(errorCell);
        tbody.appendChild(errorRow);
        spinner.style.display = "none";
      });

    // Show the modal
    modal.classList.remove("hidden");
  };

  const closeModal = () => {
    const modal = document.getElementById("paymentsModal");
    modal.classList.add("hidden");
  };

  // Attach event listeners
  document
    .getElementById("viewPendingPayments")
    ?.addEventListener("click", openPaymentsModal);

  window.closeModal = closeModal; // Expose for inline use
});
