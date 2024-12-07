/**
 * Modal Management
 */

// Open Modal
function openModal(modalId) {
  document.getElementById(modalId).classList.remove("hidden");
}

// Close Modal
function closeModal(modalId) {
  document.getElementById(modalId).classList.add("hidden");
}

/**
 * Multi-Step Form Management
 */

/**
 * Multi-Step Form Management
 */

let currentStep = 1;

// Show the desired step
function showStep(step) {
  document.querySelectorAll(".step").forEach((stepDiv, index) => {
    stepDiv.classList.toggle("hidden", index + 1 !== step);
  });
  currentStep = step;
}

// Navigate to the next step
function nextStep() {
  if (currentStep === 1) {
    completeStep1();
  } else if (currentStep === 2) {
    completeStep2();
  }
}

// Navigate to the previous step
function previousStep() {
  if (currentStep > 1) showStep(currentStep - 1);
}

// Step 1: Save Personal Details
function completeStep1() {
  const data = {
    enrollee_name: document.getElementById("enrollee_name").value,
    email: document.getElementById("email").value,
    contact_info: document.getElementById("contact_info").value,
    address: document.getElementById("address").value,
  };

  fetch("/admin/enrollee_management/add_step1", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  })
    .then((res) => res.json())
    .then((response) => {
      if (response.success) {
        console.log("Step 1 completed:", response);
        showStep(2); // Proceed to Step 2
      } else {
        alert(response.message);
      }
    })
    .catch((error) => console.error("Step 1 error:", error));
}

// Step 2: Save Course and Payment Details
function completeStep2() {
  const data = {
    course_id: document.getElementById("course_id").value,
    date_of_enrollment: document.getElementById("date_of_enrollment").value,
    payment_amount: document.getElementById("payment_amount").value,
  };

  fetch("/admin/enrollee_management/add_step2", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  })
    .then((res) => res.json())
    .then((response) => {
      if (response.success) {
        console.log("Step 2 completed:", response);
        showStep(3); // Proceed to Step 3
      } else {
        alert(response.message);
      }
    })
    .catch((error) => console.error("Step 2 error:", error));
}

// Step 3: Upload Documents
function uploadDocument(fieldName) {
  const fileInput = document.getElementById(fieldName);
  const statusSpan = document.getElementById(`${fieldName}Status`);

  if (!fileInput.files.length) {
    alert("Please select a file to upload.");
    return;
  }

  const formData = new FormData();
  formData.append(fieldName, fileInput.files[0]);

  statusSpan.innerText = "Uploading...";
  fetch(`/admin/enrollee_management/upload/${fieldName}`, {
    method: "POST",
    body: formData,
  })
    .then((res) => res.json())
    .then((response) => {
      if (response.success) {
        statusSpan.innerText = `${fieldName} uploaded successfully ✔️`;
        fileInput.disabled = true; // Prevent re-upload
      } else {
        statusSpan.innerText = `Failed to upload: ${response.message}`;
      }
    })
    .catch((error) => {
      console.error(`Error uploading ${fieldName}:`, error);
      statusSpan.innerText = "Error occurred. Try again.";
    });
}

// Submit all uploaded documents
function submitAllDocuments() {
  const statuses = [
    document.getElementById("diplomaStatus").innerText,
    document.getElementById("form137Status").innerText,
    document.getElementById("birthCertificateStatus").innerText,
  ];

  if (statuses.some((status) => !status.includes("✔️"))) {
    alert("Please upload all required documents before submitting.");
    return;
  }

  alert("Enrollment completed successfully!");
}

function viewDetails(enrolleeId) {
  // Open the modal
  openModal("enrolleeDetailsModal");

  // Fetch enrollee details
  fetch(`/admin/enrollee_management/view/${enrolleeId}`)
    .then((res) => res.json())
    .then((data) => {
      // Populate modal content
      const content = `
        <div class="grid grid-cols-2 gap-6">
          <!-- Left Column: Personal Info -->
          <div>
            <h3 class="text-lg font-semibold mb-4 text-gray-800">Personal Information</h3>
            <div class="space-y-2">
              <p><strong>Name:</strong> ${data.enrollee_name}</p>
              <p><strong>Email:</strong> ${data.email || "Not provided"}</p>
              <p><strong>Contact Info:</strong> ${data.contact_info}</p>
              <p><strong>Course:</strong> ${data.course_name}</p>
              <p><strong>Enrollment Date:</strong> ${
                data.date_of_enrollment
              }</p>
              <p class="text-green-600 font-bold"><strong>Balance:</strong> ₱${parseFloat(
                data.balance
              ).toFixed(2)}</p>
            </div>
          </div>

          <!-- Right Column: Payments -->
          <div>
            <h3 class="text-lg font-semibold mb-4 text-gray-800">Payments</h3>
            <ul class="space-y-2">
              ${
                data.payments.length > 0
                  ? data.payments
                      .map(
                        (payment) =>
                          `<li class="flex justify-between items-center bg-gray-100 p-3 rounded-lg shadow-sm">
                              <div>
                                <p class="font-medium text-gray-700">₱${parseFloat(
                                  payment.amount
                                ).toFixed(2)}</p>
                                <p class="text-sm text-gray-500">${
                                  payment.payment_date
                                } (${payment.payment_method})</p>
                              </div>
                          </li>`
                      )
                      .join("")
                  : '<p class="text-gray-500">No payments recorded.</p>'
              }
            </ul>
          </div>
        </div>

        <!-- Documents Section -->
        <h3 class="text-lg font-semibold mt-6 mb-4 text-gray-800">Documents</h3>
        <div class="grid grid-cols-3 gap-4">
          ${
            data.documents.length > 0
              ? data.documents
                  .map((doc) => {
                    const isImage = ["jpg", "jpeg", "png"].some((ext) =>
                      doc.file_path.toLowerCase().endsWith(ext)
                    );
                    return `
                      <div class="bg-gray-100 p-4 rounded-lg shadow-sm">
                        <p class="font-medium text-gray-700">${
                          doc.document_name
                        }</p>
                        ${
                          isImage
                            ? `<img src="${doc.file_path}" alt="${doc.document_name}" class="w-full h-32 object-cover mt-2 rounded-lg">`
                            : `<a href="${doc.file_path}" target="_blank" class="block mt-2 bg-blue-500 text-white text-sm px-4 py-2 text-center rounded-lg hover:bg-blue-600">View File</a>`
                        }
                      </div>
                    `;
                  })
                  .join("")
              : '<p class="text-gray-500">No documents submitted.</p>'
          }
        </div>
      `;
      document.getElementById("detailsContent").innerHTML = content;
    })
    .catch((error) => {
      console.error("Error loading enrollee details:", error);
      alert("Failed to load enrollee details. Please try again.");
    });
}
