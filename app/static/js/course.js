function openModal(modalId) {
  document.getElementById(modalId).classList.remove("hidden");
}

function closeModal(modalId) {
  document.getElementById(modalId).classList.add("hidden");
}

function editCourse(courseId) {
  fetch(`/api/get_course/${courseId}`)
    .then((res) => res.json())
    .then((data) => {
      document.getElementById("updateCourseId").value = data.id;
      document.getElementById("updateCourseName").value = data.course_name;
      document.getElementById("updateCourseDescription").value =
        data.description;
      document.getElementById("updateCourseType").value = data.type;
      document.getElementById("updateCourseQualification").value =
        data.qualification_type;
      document.getElementById("updateCourseFee").value = data.fee;
      document.getElementById("updateCourseDuration").value = data.duration;
      openModal("updateCourseModal");
    });
}

function deleteCourse(courseId) {
  console.log(`Attempting to delete course with ID: ${courseId}`); // Log courseId
  if (confirm("Are you sure you want to delete this course?")) {
    fetch(`/admin/course_management/delete/${courseId}`, {
      method: "POST",
    })
      .then((res) => {
        console.log(res); // Log the response
        if (res.ok) {
          alert("Course deleted successfully.");
          location.reload(); // Reload the page to reflect changes
        } else {
          alert("Failed to delete course. Please try again.");
        }
      })
      .catch((error) => {
        console.error("Error:", error);
        alert("An error occurred. Please try again.");
      });
  }
}

// Real-time field validation
document
  .querySelectorAll("#addCourseForm input, #addCourseForm textarea")
  .forEach((input) => {
    input.addEventListener("input", (e) => {
      if (e.target.validity.valid) {
        e.target.classList.remove("border-red-500");
      } else {
        e.target.classList.add("border-red-500");
      }
    });
  });

document.querySelector("#addCourseForm").addEventListener("submit", (e) => {
  const requiredFields = ["course_name", "description", "fee", "duration"];
  let isValid = true;

  requiredFields.forEach((fieldName) => {
    const field = document.querySelector(`[name="${fieldName}"]`);
    if (!field.value.trim()) {
      field.classList.add("border-red-500");
      isValid = false;
    }
  });

  if (!isValid) {
    e.preventDefault();
    alert("Please fill in all required fields.");
  }
});

document.querySelector("#addCourseForm").addEventListener("submit", (e) => {
  const requiredFields = ["course_name", "description", "fee", "duration"];
  let isValid = true;

  // Check required fields
  requiredFields.forEach((fieldName) => {
    const field = document.querySelector(`[name="${fieldName}"]`);
    if (!field.value.trim()) {
      field.classList.add("border-red-500");
      isValid = false;
    } else {
      field.classList.remove("border-red-500");
    }
  });

  // Check for validation errors
  const courseNameInput = document.querySelector('input[name="course_name"]');
  const errorContainer = courseNameInput
    .closest(".input-group")
    ?.querySelector(".error-message");

  if (errorContainer && !errorContainer.classList.contains("hidden")) {
    isValid = false; // Validation error exists
  }

  // Prevent form submission if validation fails
  if (!isValid) {
    e.preventDefault();
    alert("Please resolve all validation errors before submitting.");
  }
});

// Real-time duplicate course name check
document
  .querySelector('input[name="course_name"]')
  .addEventListener("blur", (e) => {
    const courseNameInput = e.target;
    const errorContainer = courseNameInput
      .closest(".input-group")
      ?.querySelector(".error-message");
    const submitButton = document.querySelector("#submitButton");

    fetch(
      `/api/check_course_name?name=${encodeURIComponent(courseNameInput.value)}`
    )
      .then((res) => res.json())
      .then((data) => {
        if (data.exists) {
          if (errorContainer) {
            errorContainer.textContent =
              "This course name already exists. Please choose a different name.";
            errorContainer.classList.remove("hidden"); // Show error
          }
          courseNameInput.classList.add("border-red-500");
          submitButton.disabled = true; // Disable the "Add" button
        } else {
          if (errorContainer) {
            errorContainer.textContent = "";
            errorContainer.classList.add("hidden"); // Hide error
          }
          courseNameInput.classList.remove("border-red-500");
          submitButton.disabled = false; // Enable the "Add" button
        }
      })
      .catch((error) => {
        console.error("Error checking course name:", error);
        // Disable the button to prevent unintended behavior
        submitButton.disabled = true;
      });
  });

// BULK DELETE

// Select All Checkboxes
function toggleAllCheckboxes() {
  const selectAll = document.getElementById("selectAll");
  const checkboxes = document.querySelectorAll(".courseCheckbox");
  checkboxes.forEach((checkbox) => (checkbox.checked = selectAll.checked));
  updateBulkDeleteButton();
}

// Update Bulk Delete Button
function updateBulkDeleteButton() {
  const selectedCheckboxes = document.querySelectorAll(
    ".courseCheckbox:checked"
  );
  const bulkDeleteButton = document.getElementById("bulkDeleteButton");
  bulkDeleteButton.disabled = selectedCheckboxes.length === 0;
}

// Bulk Delete Function
function bulkDelete() {
  const selectedCheckboxes = document.querySelectorAll(
    ".courseCheckbox:checked"
  );
  const idsToDelete = Array.from(selectedCheckboxes).map(
    (checkbox) => checkbox.value
  );

  if (
    idsToDelete.length > 0 &&
    confirm("Are you sure you want to delete the selected courses?")
  ) {
    fetch("/admin/course_management/bulk_delete", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ ids: idsToDelete }),
    })
      .then((res) => {
        if (res.ok) {
          alert("Selected courses deleted successfully.");
          location.reload();
        } else {
          alert("Failed to delete selected courses. Please try again.");
        }
      })
      .catch((error) => {
        console.error("Error:", error);
        alert("An error occurred. Please try again.");
      });
  }
}


