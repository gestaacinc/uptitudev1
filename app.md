# Sprint Plan: Course Enrollment Management System


---

## Sprint 1: **User Management**

**Goal:** Implement a secure user management module to control who can access the system and what they can do (admin vs. staff).

### Tasks

1. **Project Setup & Environment**
   - **Description:** Set up the initial project structure, install frameworks, configure database connections, and basic project config.
   - **Acceptance Criteria:** 
     - Project runs locally with a connection to the MySQL/MariaDB database.
     - Basic code structure in place (e.g., using an MVC pattern, or preferred architecture).
   - **Estimate:** 1-2 days

2. **User Registration / Creation (Admin)**
   - **Description:** Allow only an admin to create new user accounts (admin or staff).
   - **Acceptance Criteria:**
     - Endpoint/form to create a user with `email`, `password`, `role`, `full_name`.
     - Input validation (unique email, valid password strength).
   - **Estimate:** 1-2 days

3. **User Login & Authentication**
   - **Description:** Implement login functionality (session-based or token-based) for all users.
   - **Acceptance Criteria:**
     - Users can log in with valid credentials; invalid credentials result in error.
     - Passwords are securely hashed (e.g., bcrypt).
   - **Estimate:** 1-2 days

4. **Role-Based Access Control**
   - **Description:** Differentiate between admin and staff privileges.
   - **Acceptance Criteria:**
     - Admin can access restricted features (e.g., user creation, advanced settings).
     - Staff can only access enrollment/payment/document features.
   - **Estimate:** 1 day

**Expected Sprint Duration:** ~2 weeks (Adjust as needed)

---

## Sprint 2: **Course Management**

**Goal:** Provide functionality to create, update, and list available courses (Scholarship or Regular) with fees and duration.

### Tasks

1. **Course Model & CRUD**
   - **Description:** Implement basic CRUD endpoints or interfaces for `courses`.
   - **Acceptance Criteria:**
     - Admin can create new courses with `name`, `type`, `fee`, `duration`.
     - Admin can update existing courses (e.g., change fee).
     - Admin can list and view course details.
   - **Estimate:** 2-3 days

2. **Course Validation & Error Handling**
   - **Description:** Validate inputs (e.g., ensure fee is a float, duration is positive).
   - **Acceptance Criteria:**
     - Error messages are displayed on invalid input.
     - Proper status codes returned on API errors (if building an API).
   - **Estimate:** 1 day

3. **Course Deletion or Archiving (Optional)**
   - **Description:** Provide a way to retire or delete a course that is no longer offered.
   - **Acceptance Criteria:**
     - Admin can mark a course as inactive or delete it entirely (depending on your business logic).
   - **Estimate:** 1 day

**Expected Sprint Duration:** ~1-2 weeks

---

## Sprint 3: **Enrollment Management**

**Goal:** Allow staff to enroll students, update their status, and view enrollment info.

### Tasks

1. **Enrollment Creation**
   - **Description:** Implement the ability to create a new enrollment linked to a course.
   - **Acceptance Criteria:**
     - Staff can add a student with `student_name`, `course_id`, `training_type`, and an enrollment date.
     - The system either auto-generates or requires a unique `student_id`.
   - **Estimate:** 2-3 days

2. **Upload Student Photo (Optional)**
   - **Description:** Provide file upload functionality for a student’s photo, saved in the `photo` field.
   - **Acceptance Criteria:**
     - File size and format validations (e.g., PNG/JPG).
   - **Estimate:** 1-2 days

3. **View & Search Enrollments**
   - **Description:** List all enrollments and filter by name, ID, or course.
   - **Acceptance Criteria:**
     - Staff can see a table of enrollments with key info (student name, course, status).
     - Staff can quickly search or filter by student name or ID.
   - **Estimate:** 2 days

4. **Update Enrollment Status**
   - **Description:** Change the status of an enrollment (Pending -> Enrolled -> Completed -> Dropped).
   - **Acceptance Criteria:**
     - Staff can update the status; system logs the `updated_at` timestamp.
     - Completion date recorded when status = Completed.
   - **Estimate:** 1-2 days

**Expected Sprint Duration:** ~2 weeks

---

## Sprint 4: **Document Management**

**Goal:** Track required student documents (high school proof, TOR, etc.) and mark completeness.

### Tasks

1. **Documents Model & Linking**
   - **Description:** Create a linked record of documents for each enrollment (`enrollment_id`).
   - **Acceptance Criteria:**
     - When a new enrollment is created, a corresponding documents entry is auto-generated or staff can manually add one.
   - **Estimate:** 1 day

2. **Document Submission & Status**
   - **Description:** Staff can mark each required document (e.g., `high_school_proof`, `valid_id`, etc.) as submitted.
   - **Acceptance Criteria:**
     - Each document is stored as a boolean/tinyint field (1 for submitted, 0 for missing).
     - Overall `status` set to `Complete` or `Incomplete`.
   - **Estimate:** 2 days

3. **Document Viewing & Incomplete Alerts**
   - **Description:** Provide a view or checklist that shows which documents are missing for a given enrollment.
   - **Acceptance Criteria:**
     - Staff can quickly see a summary of missing documents (optional: highlight or flag if incomplete).
   - **Estimate:** 1-2 days

**Expected Sprint Duration:** ~1 week

---

## Sprint 5: **Payment Management**

**Goal:** Manage tuition/fee payments (downpayment, installments, additional fees).

### Tasks

1. **Create Payment Records**
   - **Description:** Link `payments` to an existing `enrollment_id`. Allow staff to record partial or full payments.
   - **Acceptance Criteria:**
     - Staff can enter payment amounts (downpayment, second payment, third payment, etc.).
     - Payment method is recorded (`Cash`, `GCash`, `Online Bank Transfer`).
   - **Estimate:** 2-3 days

2. **Calculate & Track Balance**
   - **Description:** Implement logic to calculate the remaining balance based on recorded payments and total fee.
   - **Acceptance Criteria:**
     - System automatically updates `balance` each time a payment is logged.
   - **Estimate:** 1-2 days

3. **Additional Fees (Assessment & TESDA Cert)**
   - **Description:** Allow staff to mark if `assessment_fee_paid` or `tesda_cert_paid` is completed.
   - **Acceptance Criteria:**
     - Boolean fields for each additional fee; staff can toggle paid/unpaid.
   - **Estimate:** 1 day

4. **View Payment History**
   - **Description:** Show a summary of all payments for a specific enrollment, including timestamps.
   - **Acceptance Criteria:**
     - Staff can see a chronological list of partial payments.
     - Display any outstanding balance or overdue fees if applicable.
   - **Estimate:** 2 days

**Expected Sprint Duration:** ~2 weeks

---

## Sprint 6: **Reporting & Administration**

**Goal:** Provide basic dashboards and reports for enrollments, payments, and documents. Finalize system administration tasks.

### Tasks

1. **Enrollment Report**
   - **Description:** Show the number of students per course, filterable by status.
   - **Acceptance Criteria:**
     - A simple dashboard or table with aggregated counts (e.g., total enrolled in each course).
   - **Estimate:** 2-3 days

2. **Payment Report**
   - **Description:** Summarize total collected fees vs. outstanding balances for a given time period.
   - **Acceptance Criteria:**
     - Chart or table showing sums of payments grouped by month or date range.
   - **Estimate:** 2-3 days

3. **Document Compliance Report**
   - **Description:** Show how many enrollments are missing documents or have incomplete submissions.
   - **Acceptance Criteria:**
     - List or chart of incomplete vs. complete documents across all enrollments.
   - **Estimate:** 2 days

4. **System Administration / Maintenance**
   - **Description:** Implement logs, backups, or advanced admin settings (if needed).
   - **Acceptance Criteria:**
     - Automated DB backups scheduled (if in scope).
     - Admin-only page to view system logs or user activity (if in scope).
   - **Estimate:** 2+ days (depends on scope)

**Expected Sprint Duration:** ~2-3 weeks

---

## Optional Future Sprints

- **Sprint X: UI/UX Enhancements**  
  - Refine front-end design, navigation, and usability.
- **Sprint Y: Notifications / Email Integration**  
  - Send automated emails to students for incomplete documents or payment reminders.
- **Sprint Z: Advanced Permissions**  
  - More granular roles beyond just “admin” and “staff.”

---

# Summary

This **six-sprint plan** covers the key features implied by the SQL schema:
1. **User Management**  
2. **Course Management**  
3. **Enrollment Management**  
4. **Document Management**  
5. **Payment Management**  
6. **Reporting & Administration**

 
