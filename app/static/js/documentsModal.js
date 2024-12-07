document.addEventListener("DOMContentLoaded", () => {
  /**
   * Open the Documents Modal and fetch data dynamically.
   */
  const openDocumentsModal = () => {
    const modal = document.getElementById("documentsModal");
    const spinner = modal.querySelector(".loader");
    const table = modal.querySelector("table");
    const tbody = modal.querySelector("tbody");

    // Reset modal content
    spinner.style.display = "flex";
    table.style.display = "none";
    tbody.innerHTML = "";

    // Fetch data from the documents endpoint
    fetch("/admin/pending_documents")
      .then((response) => response.json())
      .then((data) => {
        // Populate the table with fetched data
        data.forEach((item) => {
          const row = document.createElement("tr");

          row.className = "hover:bg-gray-50"; // TailwindCSS class for hover effect

          // Enrollee Name Cell
          const enrolleeCell = document.createElement("td");
          enrolleeCell.className = "border px-4 py-2 text-gray-800";
          enrolleeCell.textContent = item.enrollee_name;
          row.appendChild(enrolleeCell);

          // Course Name Cell
          const courseCell = document.createElement("td");
          courseCell.className = "border px-4 py-2 text-gray-800";
          courseCell.textContent = item.course_name;
          row.appendChild(courseCell);

          // Document Name Cell
          const documentCell = document.createElement("td");
          documentCell.className = "border px-4 py-2 text-gray-800";
          documentCell.textContent = item.document_name;
          row.appendChild(documentCell);

          tbody.appendChild(row);
        });

        // Hide spinner and show table
        spinner.style.display = "none";
        table.style.display = "table";
      })
      .catch((error) => {
        console.error("Error fetching documents data:", error);

        // Display an error message
        const errorRow = document.createElement("tr");
        const errorCell = document.createElement("td");
        errorCell.colSpan = 3; // Adjust for your table columns
        errorCell.className = "text-red-500 text-center px-4 py-2";
        errorCell.textContent = "An error occurred while fetching data.";
        errorRow.appendChild(errorCell);
        tbody.appendChild(errorRow);

        spinner.style.display = "none";
      });

    // Show the modal
    modal.classList.remove("hidden");
  };

  /**
   * Close the Documents Modal.
   */
  const closeDocumentsModal = () => {
    const modal = document.getElementById("documentsModal");
    modal.classList.add("hidden");
  };

  // Attach event listeners to open and close buttons
  document
    .getElementById("viewPendingDocuments")
    ?.addEventListener("click", openDocumentsModal);

  document
    .getElementById("closeDocumentsModal")
    ?.addEventListener("click", closeDocumentsModal);

  // Attach event listener to close icon
  document
    .querySelector("#documentsModal .close-icon")
    ?.addEventListener("click", closeDocumentsModal);
});
