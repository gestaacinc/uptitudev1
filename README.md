
## **Database Schema**

### **1. Staff Table**
```sql
CREATE TABLE staff (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    email VARCHAR(255) UNIQUE,
    password VARCHAR(255),
    role ENUM('admin', 'finance', 'staff') DEFAULT 'staff',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

### **2. Courses Table**
```sql
CREATE TABLE courses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    course_name VARCHAR(255), -- Name of the course
    type ENUM('TESDA', 'Regular') DEFAULT 'TESDA', -- TESDA or Regular
    qualification_type ENUM('NC1', 'NC2', 'NC3', 'NTR') DEFAULT 'NTR', -- TESDA qualification level
    fee DECIMAL(10, 2), -- Training fee
    assessment_fee DECIMAL(10, 2), -- Fee for assessment
    duration INT, -- Duration in days
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

### **3. Enrollees Table**
```sql
CREATE TABLE enrollees (
    id INT AUTO_INCREMENT PRIMARY KEY,
    enrollee_name VARCHAR(255), -- Name of the enrollee
    contact_info VARCHAR(50), -- Contact details of the enrollee
    course_id INT, -- Links enrollee to a specific course
    enrollment_status ENUM('Pending', 'Ongoing', 'Completed') DEFAULT 'Pending', -- Enrollment status
    total_fee DECIMAL(10, 2), -- Total training fee (from courses table)
    balance DECIMAL(10, 2) DEFAULT 0.00, -- Remaining balance
    tesda_cert_fee DECIMAL(10, 2) DEFAULT 35.00, -- Fixed TESDA certification fee
    FOREIGN KEY (course_id) REFERENCES courses(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

### **4. Payments Table**
```sql
CREATE TABLE payments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    enrollee_id INT, -- Links payment to a specific enrollee
    payment_date DATE, -- Date of payment
    payment_type ENUM('Down Payment', 'Second Payment', 'Third Payment'), -- Type of payment
    amount DECIMAL(10, 2), -- Amount paid
    payment_method ENUM('Cash', 'GCash', 'Bank Transfer'), -- Payment method used
    payment_for ENUM('Training', 'Assessment', 'TESDA Certification') DEFAULT 'Training', -- Purpose of the payment
    FOREIGN KEY (enrollee_id) REFERENCES enrollees(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

### **5. Fee Breakdown Table** *(Optional, for advanced reporting or tracking additional fees)*
```sql
CREATE TABLE fee_breakdowns (
    id INT AUTO_INCREMENT PRIMARY KEY,
    enrollee_id INT, -- Links to specific enrollee
    fee_type ENUM('Assessment', 'TESDA Certification'), -- Fee type
    amount DECIMAL(10, 2), -- Amount for the fee
    FOREIGN KEY (enrollee_id) REFERENCES enrollees(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### **6. Document Tracking Table**
```sql
CREATE TABLE documents (
    id INT AUTO_INCREMENT PRIMARY KEY,
    enrollee_id INT, -- Links document submission to a specific enrollee
    document_name VARCHAR(255), -- Name of the required document
    submitted BOOLEAN DEFAULT FALSE, -- Tracks if the document has been submitted
    FOREIGN KEY (enrollee_id) REFERENCES enrollees(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

### **7. Audit Logs Table**
```sql
CREATE TABLE audit_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    staff_id INT, -- Tracks which staff member performed the action
    action VARCHAR(255), -- Description of the action
    details TEXT, -- Additional details about the action
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (staff_id) REFERENCES staff(id)
);
```

---

## **Features Using User Stories**

### **1. Course Management**
- **As an admin**, I want to add, update, and delete courses, so that I can manage all training and TESDA courses.
- **As an admin**, I want to specify the TESDA qualification type (NC1, NC2, NC3, or NTR) for each course, so that courses are properly categorized.
- **As an admin**, I want to set course-specific fees and durations, so that I can track costs and timelines effectively.

---

### **2. Enrollee Management**
- **As a staff member**, I want to register enrollees and assign them to specific courses, so that I can track their progress and payments.
- **As a staff member**, I want to update the enrollment status of enrollees (Pending, Ongoing, Completed), so that I can monitor their current stage in the training.
- **As a staff member**, I want to view enrollees' outstanding balances, so that I can follow up on overdue payments.

---

### **3. Payment Tracking**
- **As a staff member**, I want to record payments for training, assessment, and TESDA certification, so that I can ensure all payments are accounted for.
- **As a staff member**, I want to differentiate between payment types (Down Payment, Second Payment, Third Payment), so that I can track payment progress.
- **As a staff member**, I want to see the payment methods (Cash, GCash, Bank Transfer) used by enrollees, so that I can generate payment method-specific reports.
- **As a staff member**, I want to automatically calculate remaining balances after each payment, so that I don’t have to manually update records.

---

### **4. Document Tracking**
- **As a staff member**, I want to monitor the submission status of required documents, so that I can identify missing documents and follow up with enrollees.
- **As a staff member**, I want to generate a report of enrollees with incomplete documents, so that I can ensure compliance before the training begins.

---

### **5. Fee Management**
- **As an admin**, I want to define the TESDA certification fee (PHP 35) and course-specific assessment fees, so that these costs are automatically included in the enrollee’s total fee.
- **As a staff member**, I want to track payments for assessment and TESDA certification fees separately, so that I can easily generate fee-specific financial reports.

---

### **6. Reporting**
- **As an admin**, I want to generate reports on enrollees grouped by TESDA qualification type (NC1, NC2, NC3, NTR), so that I can submit required information to TESDA.
- **As a staff member**, I want to generate a report of outstanding balances for all enrollees, so that I can prioritize follow-ups on overdue accounts.
- **As an admin**, I want to export financial and enrollment reports to Excel or PDF, so that I can share them with management.

---

### **7. Audit Logs**
- **As an admin**, I want to see a log of all actions performed by staff, so that I can ensure accountability for data updates and changes.
- **As an admin**, I want to track who made changes to enrollee or payment records, so that I can identify errors or inconsistencies.

---

### **8. User Roles**
- **As an admin**, I want to assign roles (Admin, Finance, Staff) to system users, so that I can restrict access based on responsibilities.
- **As a staff member**, I want to access only the features related to my role, so that I don’t accidentally modify restricted data.

---

## **Next Steps**
1. Begin implementing the database schema using MySQL.
2. Start with **Course Management** (CRUD for courses).
3. Gradually move to **Enrollee Management** and **Payment Tracking**.
4. Let me know if you’d like step-by-step guidance for any phase!
