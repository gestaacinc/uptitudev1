from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from enum import Enum

# Enums for roles and statuses
class UserRole(Enum):
    ADMIN = 'ADMIN'
    FINANCE = 'FINANCE'
    STAFF = 'STAFF'

class UserStatus(Enum):
    ACTIVE = 'active'
    INACTIVE = 'inactive'

class Staff(db.Model):
    __tablename__ = 'staff'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True, index=True)
    password_hash = db.Column(db.String(255))
    role = db.Column(db.Enum(UserRole), default=UserRole.STAFF.value)
    login_attempts = db.Column(db.Integer, default=0)
    lockout_until = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.Enum(UserStatus), default=UserStatus.ACTIVE.value)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    updated_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    @property
    def password(self):
        raise AttributeError('Password is not readable!')

    @password.setter
    def password(self, plain_password):
        self.password_hash = generate_password_hash(plain_password)

    def verify_password(self, plain_password):
        return check_password_hash(self.password_hash, plain_password)

    def set_password(self, plain_password):  # Add this for compatibility
        self.password_hash = generate_password_hash(plain_password)

    def __repr__(self):
        return f"<Staff {self.name} ({self.email})>"

    
# Courses Model
class Course(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(255), unique=True)
    description = db.Column(db.Text)
    type = db.Column(db.Enum('TESDA', 'Regular'), default='TESDA')
    qualification_type = db.Column(db.Enum('NC1', 'NC2', 'NC3', 'NTR'), default='NTR')
    fee = db.Column(db.Numeric(10, 2))
    assessment_fee = db.Column(db.Numeric(10, 2))
    duration = db.Column(db.Integer)
    status = db.Column(db.Enum('active', 'archived'), default='active')
    created_by = db.Column(db.Integer, db.ForeignKey('staff.id'))  # NEW
    updated_by = db.Column(db.Integer, db.ForeignKey('staff.id'))  # NEW
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    updated_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

# Updated Enrollees Model
class Enrollee(db.Model):
    __tablename__ = 'enrollees'
    id = db.Column(db.Integer, primary_key=True)
    enrollee_name = db.Column(db.String(255))
    email = db.Column(db.String(255), nullable=True)
    contact_info = db.Column(db.String(50))
    photo_path = db.Column(db.String(255), nullable=True)
    address = db.Column(db.Text, nullable=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
    enrollment_status = db.Column(db.Enum('Pending', 'Ongoing', 'Completed'), default='Pending')
    total_fee = db.Column(db.Numeric(10, 2))
    balance = db.Column(db.Numeric(10, 2), default=0.00)
    completion_date = db.Column(db.Date, nullable=True)
    date_of_enrollment = db.Column(db.Date)  # Ensure this exists
    created_by = db.Column(db.Integer, db.ForeignKey('staff.id'))
    updated_by = db.Column(db.Integer, db.ForeignKey('staff.id'))
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    updated_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    # Define the relationship to the Course model
    course = db.relationship('Course', backref='enrollees')



# Payments Model
class Payment(db.Model):
    __tablename__ = 'payments'
    id = db.Column(db.Integer, primary_key=True)
    enrollee_id = db.Column(db.Integer, db.ForeignKey('enrollees.id'))
    payment_date = db.Column(db.Date)
    payment_type = db.Column(db.Enum('Down Payment', 'Second Payment', 'Third Payment'))
    amount = db.Column(db.Numeric(10, 2))
    payment_method = db.Column(db.Enum('Cash', 'GCash', 'Bank Transfer'))
    transaction_id = db.Column(db.String(255), nullable=True)
    payment_for = db.Column(db.Enum('Training', 'Assessment', 'TESDA Certification'), default='Training')
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    updated_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

# Updated Documents Model
class Document(db.Model):
    __tablename__ = 'documents'
    id = db.Column(db.Integer, primary_key=True)
    enrollee_id = db.Column(db.Integer, db.ForeignKey('enrollees.id'))
    document_name = db.Column(db.String(255))
    required_by = db.Column(db.Date, nullable=True)
    submitted = db.Column(db.Boolean, default=False)
    status = db.Column(db.Enum('Pending', 'Incomplete', 'Approved'), default='Pending')  # NEW
    file_path = db.Column(db.String(255), nullable=True)
    uploaded_at = db.Column(db.TIMESTAMP, nullable=True)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    updated_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    
# Audit Logs Model
class AuditLog(db.Model):
    __tablename__ = 'audit_logs'
    id = db.Column(db.Integer, primary_key=True)
    staff_id = db.Column(db.Integer, db.ForeignKey('staff.id'))
    action = db.Column(db.String(255))
    details = db.Column(db.Text)
    module = db.Column(db.Enum('courses', 'enrollees', 'payments', 'documents'))
    ip_address = db.Column(db.String(45), nullable=True)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())

# Updated Fee Breakdown Model
class FeeBreakdown(db.Model):
    __tablename__ = 'fee_breakdowns'
    id = db.Column(db.Integer, primary_key=True)
    enrollee_id = db.Column(db.Integer, db.ForeignKey('enrollees.id'))
    fee_type = db.Column(db.Enum('Assessment', 'TESDA Certification'))
    amount = db.Column(db.Numeric(10, 2))
    description = db.Column(db.String(255), nullable=True)  # NEW
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())

# Notifications Model
class Notification(db.Model):
    __tablename__ = 'notifications'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    message = db.Column(db.Text)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
