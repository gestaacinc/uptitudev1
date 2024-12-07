from decimal import Decimal
import os
import re
from flask import jsonify, render_template, request, redirect, url_for, flash, session
from itsdangerous import URLSafeTimedSerializer,SignatureExpired, BadSignature
from app import app, db, mail
from app.models import Payment, Staff
import smtplib
from email.mime.text import MIMEText
from flask_mail import Message
from app.models import Enrollee, Course, Document
from sqlalchemy import func
from datetime import date, datetime, timedelta
from sqlalchemy.exc import IntegrityError
from sqlalchemy import or_, and_

@app.route('/', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Debug: Check if email and password are provided
        if not email or not password:
            flash('Email and password are required.', 'danger')
            return render_template('admin_login.html', title="Admin Login")

        # Check if the user exists
        user = Staff.query.filter_by(email=email).first()
        if user:
            # Debug: Check if the password hash exists
            if not user.password_hash:
                flash('No password set for this user.', 'danger')
                return render_template('admin_login.html', title="Admin Login")

            # Verify the password
            if user.verify_password(password):
                # Save user details in the session
                session['user_id'] = user.id
                session['user_name'] = user.name
                session['role'] = user.role.value  # Save Enum as a string
                flash('Login successful!', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid password.', 'danger')
        else:
            flash('Invalid email.', 'danger')

    return render_template('admin_login.html', title="Admin Login")


@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('admin_login'))

# -----------FORGOT PASSWORD --------------

def send_email(subject, recipients, body):
    msg = Message(subject, recipients=recipients)
    msg.body = body
    mail.send(msg)

@app.route('/forgot_password', methods=['POST'])
def forgot_password():
    email = request.form.get('email')

    if not email:
        return {"status": "error", "message": "Email is required."}, 400

    try:
        user = Staff.query.filter_by(email=email).first()

        if not user:
            return {"status": "error", "message": "Email not found. Please try again."}, 404

        # Generate Reset Token
        serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        token = serializer.dumps(email, salt='password-reset-salt')

        # Create Reset Link
        reset_link = f"http://{request.host}/reset_password/{token}"

        # Log the reset link and email for debugging
        print(f"Reset link: {reset_link}")
        print(f"Email: {email}")

        # Send Email
        subject = "Password Reset Request"
        body = f"Hello,\n\nPlease click the link below to reset your password:\n\n{reset_link}"
        send_email(subject, [email], body)

        return {"status": "success", "message": "Password reset email sent! Check your inbox."}, 200
    except Exception as e:
        print(f"Error in forgot_password route: {e}")
        return {"status": "error", "message": "An error occurred. Please try again later."}, 500

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    
    try:
        # Decode the token
        email = serializer.loads(token, salt='password-reset-salt', max_age=3600)  # 1 hour expiry
    except SignatureExpired:
        flash('The password reset link has expired. Please request a new one.', 'danger')
        return redirect(url_for('forgot_password'))
    except BadSignature:
        flash('Invalid password reset link.', 'danger')
        return redirect(url_for('forgot_password'))

    if request.method == 'POST':
        # Get the new password from the form
        new_password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if new_password != confirm_password:
            flash('Passwords do not match. Please try again.', 'danger')
            return render_template('reset_password.html', token=token)

        # Find the user by email and update their password
        user = Staff.query.filter_by(email=email).first()
        if user:
            user.set_password(new_password)  # Assumes you have a `set_password` method
            db.session.commit()
            flash('Your password has been reset successfully. Please log in.', 'success')
            return redirect(url_for('admin_login'))
        else:
            flash('An error occurred. Please try again.', 'danger')

    return render_template('reset_password.html', token=token)

 #------------ADMIN DASHBOARD
@app.route('/admin/dashboard')
def dashboard():
    # Total Enrollees
    total_enrollees = Enrollee.query.count() or 0
    enrollees_last_month = (
        Enrollee.query.filter(
            Enrollee.created_at.between(
                date.today() - timedelta(days=60), date.today() - timedelta(days=30)
            )
        ).count()
        or 0
    )
    enrollee_growth = (
        ((total_enrollees - enrollees_last_month) / enrollees_last_month * 100)
        if enrollees_last_month > 0
        else 0
    )

    # Active Courses
    active_courses = Course.query.filter_by(status='active').count() or 0
    courses_last_month = (
        Course.query.filter(
            Course.updated_at.between(
                date.today() - timedelta(days=60), date.today() - timedelta(days=30)
            )
        ).count()
        or 0
    )
    course_change = (
        ((active_courses - courses_last_month) / courses_last_month * 100)
        if courses_last_month > 0
        else 0
    )

    # Pending Payments
    pending_payments = (
        db.session.query(func.sum(Enrollee.balance))
        .filter(Enrollee.balance > 0)
        .scalar()
        or 0
    )
    payments_last_month = (
        db.session.query(func.sum(Enrollee.balance))
        .filter(
            Enrollee.created_at.between(
                date.today() - timedelta(days=60), date.today() - timedelta(days=30)
            ),
            Enrollee.balance > 0,
        )
        .scalar()
        or 0
    )
    payment_growth = (
        ((payments_last_month - pending_payments) / payments_last_month * 100)
        if payments_last_month > 0
        else 0
    )

    # Pending Documents
    pending_documents = (
        Document.query.filter((Document.submitted == 0) | (Document.submitted.is_(None))).count()
        or 0
    )
    documents_last_month = (
        Document.query.filter(
            Document.created_at.between(
                date.today() - timedelta(days=60), date.today() - timedelta(days=30)
            ),
            (Document.submitted == 0) | (Document.submitted.is_(None)),
        ).count()
        or 0
    )
    document_change = (
        ((documents_last_month - pending_documents) / documents_last_month * 100)
        if documents_last_month > 0
        else 0
    )

    # Dates
    start_date = (date.today() - timedelta(days=30)).strftime("%B %d, %Y")
    current_date = date.today().strftime("%B %d, %Y")

    return render_template(
        'admin/dashboard.html',
        title="Dashboard",
        start_date=start_date,
        current_date=current_date,
        total_enrollees=total_enrollees,
        enrollee_growth=enrollee_growth,
        active_courses=active_courses,
        course_change=course_change,
        pending_payments=pending_payments,
        payment_growth=payment_growth,
        pending_documents=pending_documents,
        document_change=document_change,
    )



@app.route('/admin/pending_payments')
def pending_payments():
    pending_payments_details = (
        db.session.query(
            Enrollee.enrollee_name, 
            Course.course_name, 
            Enrollee.balance
        )
        .join(Course, Enrollee.course_id == Course.id)
        .filter(Enrollee.balance > 0)
        .all()
    )
    return jsonify([
        {
            "enrollee_name": p.enrollee_name,
            "course_name": p.course_name,
            "pending_balance": f"₱{p.balance:.2f}"  # Use a unique key
        }
        for p in pending_payments_details
    ])


@app.route('/admin/pending_documents')
def pending_documents():
    pending_documents_details = (
        db.session.query(
            Enrollee.enrollee_name, 
            Course.course_name, 
            Document.document_name
        )
        .join(Enrollee, Document.enrollee_id == Enrollee.id)
        .join(Course, Enrollee.course_id == Course.id)
        .filter((Document.submitted == 0) | (Document.submitted.is_(None)))
        .all()
    )
    return jsonify([
        {
            "enrollee_name": d.enrollee_name,
            "course_name": d.course_name,
            "document_name": d.document_name  # Use a unique key
        }
        for d in pending_documents_details
    ])

# Route: Course Management Page
@app.route('/admin/course_management', methods=['GET'])
def course_management():
    page = request.args.get('page', 1, type=int)  # Get the page number from the URL, default is 1
    per_page = 5  # Number of courses per page
    pagination = Course.query.paginate(page=page, per_page=per_page, error_out=False)
    courses = pagination.items
    return render_template(
        'admin/course_management.html', 
        courses=courses, 
        pagination=pagination
    )

# Adding Course
@app.route('/admin/course_management/add', methods=['POST'])
def add_course():
    try:
        # Get form data
        course_name = request.form.get('course_name', '').strip()
        description = request.form.get('description', '').strip()
        type = request.form.get('type', '').strip()
        qualification_type = request.form.get('qualification_type', '').strip()
        fee = request.form.get('fee', '').strip()
        duration = request.form.get('duration', '').strip()

        # Backend validation
        errors = []

        if not course_name:
            errors.append("Course Name is required.")
        elif len(course_name) > 255:
            errors.append("Course Name cannot exceed 255 characters.")

        if not description:
            errors.append("Description is required.")
        elif len(description) > 500:
            errors.append("Description cannot exceed 500 characters.")

        if not fee or not fee.replace('.', '', 1).isdigit() or float(fee) <= 0:
            errors.append("Fee must be a positive number.")

        if not duration or not duration.isdigit() or int(duration) <= 0:
            errors.append("Duration must be a positive integer.")

        if type not in ['TESDA', 'Regular']:
            errors.append("Invalid Course Type.")

        if qualification_type not in ['NC1', 'NC2', 'NC3', 'NTR']:
            errors.append("Invalid Qualification Type.")

        if errors:
            for error in errors:
                flash(error, "error")
            return redirect(url_for('course_management'))

        # Check for duplicates
        existing_course = Course.query.filter_by(course_name=course_name).first()
        if existing_course:
            flash("A course with this name already exists.", "error")
            return redirect(url_for('course_management'))

        # Add course to the database
        course = Course(
            course_name=course_name,
            description=description,
            type=type,
            qualification_type=qualification_type,
            fee=float(fee),
            duration=int(duration),
        )
        db.session.add(course)
        db.session.commit()
        flash("Course added successfully.", "success")
    except IntegrityError:
        db.session.rollback()
        flash("A database integrity error occurred while adding the course.", "error")
    except Exception as e:
        db.session.rollback()
        flash(f"An unexpected error occurred: {str(e)}", "error")

    return redirect(url_for('course_management'))

@app.route('/api/check_course_name', methods=['GET'])
def check_course_name():
    course_name = request.args.get('name')
    if not course_name:
        return jsonify({"error": "Course name is required"}), 400

    exists = Course.query.filter_by(course_name=course_name).first() is not None
    return jsonify({"exists": exists})


# Route: Update Course
@app.route('/admin/course_management/update', methods=['POST'])
def update_course():
    try:
        course_id = request.form['course_id']
        course = Course.query.get(course_id)

        if not course:
            flash("Course not found.", "error")
            return redirect(url_for('course_management'))

        # Update course details
        course.course_name = request.form['course_name']
        course.description = request.form['description']
        course.type = request.form['type']
        course.qualification_type = request.form['qualification_type']
        course.fee = request.form['fee']
        course.duration = request.form['duration']

        db.session.commit()
        flash("Course updated successfully.", "success")
    except Exception as e:
        flash(f"Error updating course: {str(e)}", "error")
    return redirect(url_for('course_management'))

# Route: Delete Course
@app.route('/admin/course_management/delete/<int:course_id>', methods=['POST'])
def delete_course(course_id):
    try:
        course = Course.query.get(course_id)
        if not course:
            flash("Course not found.", "error")
            return redirect(url_for('course_management'))
        db.session.delete(course)
        db.session.commit()
        flash("Course deleted successfully.", "success")
    except Exception as e:
        flash(f"Error deleting course: {str(e)}", "error")
    return redirect(url_for('course_management'))


# Route: Bulk Delete Courses
@app.route('/admin/course_management/bulk_delete', methods=['POST'])
def bulk_delete_courses():
    try:
        data = request.get_json()
        course_ids = data.get('ids', [])

        if not course_ids:
            return jsonify({"error": "No course IDs provided."}), 400

        Course.query.filter(Course.id.in_(course_ids)).delete(synchronize_session=False)
        db.session.commit()
        return jsonify({"success": True}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500




# API Route: Get Course Data
@app.route('/api/get_course/<int:course_id>', methods=['GET'])
def get_course(course_id):
    course = Course.query.get(course_id)
    if not course:
        return jsonify({'error': 'Course not found'}), 404

    return jsonify({
        'id': course.id,
        'course_name': course.course_name,
        'description': course.description,
        'type': course.type,
        'qualification_type': course.qualification_type,
        'fee': str(course.fee),
        'duration': course.duration,
    })




# @app.route('/admin/enrollee_management', methods=['GET'])
# def enrollee_management():
#     # Pagination setup
#     page = request.args.get('page', 1, type=int)
#     per_page = 5

#     # Filters
#     search = request.args.get('search', '').strip()
#     start_date = request.args.get('start_date', '').strip()
#     end_date = request.args.get('end_date', '').strip()

#     # Base query
#     query = Enrollee.query

#     # Apply search filter
#     if search:
#         query = query.filter(
#             or_(
#                 Enrollee.enrollee_name.like(f"%{search}%"),
#                 Enrollee.email.like(f"%{search}%"),
#                 Enrollee.contact_info.like(f"%{search}%"),
#                 Enrollee.course.has(Course.course_name.like(f"%{search}%"))
#             )
#         )

#     # Apply date filters
#     if start_date and not end_date:
#         # Filter for start date only
#         try:
#             start_date_parsed = datetime.strptime(start_date, '%Y-%m-%d').date()
#             query = query.filter(Enrollee.date_of_enrollment == start_date_parsed)
#         except ValueError:
#             flash("Invalid start date format. Please use YYYY-MM-DD.", "error")
#     elif end_date and not start_date:
#         # Filter for end date only
#         try:
#             end_date_parsed = datetime.strptime(end_date, '%Y-%m-%d').date()
#             query = query.filter(Enrollee.date_of_enrollment <= end_date_parsed)
#         except ValueError:
#             flash("Invalid end date format. Please use YYYY-MM-DD.", "error")
#     elif start_date and end_date:
#         # Filter for range [start_date, end_date]
#         try:
#             start_date_parsed = datetime.strptime(start_date, '%Y-%m-%d').date()
#             end_date_parsed = datetime.strptime(end_date, '%Y-%m-%d').date()
#             query = query.filter(
#                 and_(
#                     Enrollee.date_of_enrollment >= start_date_parsed,
#                     Enrollee.date_of_enrollment <= end_date_parsed
#                 )
#             )
#         except ValueError:
#             flash("Invalid date range format. Please use YYYY-MM-DD.", "error")

#     # Pagination
#     enrollees_pagination = query.paginate(page=page, per_page=per_page, error_out=False)

#     # Fetch active courses
#     courses = Course.query.filter_by(status='active').all()

#     return render_template(
#         'admin/enrollment/enrollee_management.html',
#         title='Enrollee Management',
#         enrollees=enrollees_pagination.items,
#         pagination=enrollees_pagination,
#         courses=courses,
#         start_date=start_date,
#         end_date=end_date,
#         search=search,
#     )

# ENROLLMENT PAGE

# ##### enrollment page ######
@app.route('/admin/enrollee_management', methods=['GET'])
def enrollee_management():
    # Pagination and filters setup
    page = request.args.get('page', 1, type=int)
    per_page = 5
    search = request.args.get('search', '').strip()
    start_date = request.args.get('start_date', '').strip()
    end_date = request.args.get('end_date', '').strip()

    query = Enrollee.query

    # Apply filters
    if search:
        query = query.filter(
            or_(
                Enrollee.enrollee_name.like(f"%{search}%"),
                Enrollee.email.like(f"%{search}%"),
                Enrollee.contact_info.like(f"%{search}%"),
                Enrollee.course.has(Course.course_name.like(f"%{search}%"))
            )
        )
    if start_date:
        start_date_parsed = datetime.strptime(start_date, '%Y-%m-%d').date()
        query = query.filter(Enrollee.date_of_enrollment >= start_date_parsed)
    if end_date:
        end_date_parsed = datetime.strptime(end_date, '%Y-%m-%d').date()
        query = query.filter(Enrollee.date_of_enrollment <= end_date_parsed)

    enrollees_pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    courses = Course.query.filter_by(status='active').all()
    required_documents = Document.query.all()

    return render_template(
        'admin/enrollment/enrollee_management.html',
        title="Enrollee Management",
        enrollees=enrollees_pagination.items,
        pagination=enrollees_pagination,
        courses=courses,
        required_documents=required_documents,
        search=search,
        start_date=start_date,
        end_date=end_date
    )


def save_document(enrollee_id, uploaded_file):
    """Saves the uploaded document and returns the file path."""
    allowed_extensions = ['pdf', 'jpg', 'jpeg', 'png']
    if uploaded_file.filename.split('.')[-1].lower() not in allowed_extensions:
        raise ValueError("Invalid file type.")

    file_folder = os.path.join(app.config['UPLOAD_FOLDER'], str(enrollee_id))
    os.makedirs(file_folder, exist_ok=True)  # Ensure the folder exists
    file_path = os.path.join(file_folder, uploaded_file.filename)
    uploaded_file.save(file_path)

    # Save the document record to the database
    document = Document(
        enrollee_id=enrollee_id,
        document_name=uploaded_file.filename,
        file_path=file_path,
        status="Pending",
    )
    db.session.add(document)
    return file_path


# ##### enrollment saving page ######
@app.route('/admin/enrollee_management/add', methods=['POST'])
def add_enrollee():
    try:
        # Step 1: Extract Personal Details
        enrollee_name = request.form.get('enrollee_name')
        email = request.form.get('email')
        contact_info = request.form.get('contact_info')
        address = request.form.get('address')

        # Step 2: Extract Course and Payment Details
        course_id = request.form.get('course_id')
        date_of_enrollment = request.form.get('date_of_enrollment')
        payment_method = request.form.get('payment_method')
        payment_amount = request.form.get('payment_amount')

        # Validate and process enrollment
        course = Course.query.get(course_id)
        if not course:
            flash("Invalid course selected.", "error")
            return redirect(url_for('enrollee_management'))

        # Convert payment_amount to Decimal
        payment_amount_decimal = Decimal(payment_amount)

        # Calculate completion date
        enrollment_date = datetime.strptime(date_of_enrollment, '%Y-%m-%d').date()
        completion_date = enrollment_date + timedelta(days=course.duration)

        # Create enrollee object
        enrollee = Enrollee(
            enrollee_name=enrollee_name,
            email=email,
            contact_info=contact_info,
            address=address,
            course_id=course.id,
            date_of_enrollment=enrollment_date,
            completion_date=completion_date,  # Set completion date
            balance=course.fee - payment_amount_decimal
        )
        db.session.add(enrollee)
        db.session.commit()

        # Save payment details
        if payment_amount_decimal > 0:
            payment = Payment(
                enrollee_id=enrollee.id,
                payment_date=datetime.now(),
                payment_type="Down Payment",
                amount=payment_amount_decimal,
                payment_method=payment_method
            )
            db.session.add(payment)

        # Step 3: Handle Document Uploads
        documents = request.files.getlist('documents[]')
        for doc_file in documents:
            save_document(enrollee.id, doc_file)  # Call the save_document helper function

        db.session.commit()
        flash("Enrollee added successfully!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"An error occurred: {e}", "error")
    return redirect(url_for('enrollee_management'))



# STEP 1
@app.route('/admin/enrollee_management/add_step1', methods=['POST'])
def add_enrollee_step1():
    try:
        data = request.json
        enrollee = Enrollee(
            enrollee_name=data['enrollee_name'],
            email=data.get('email'),
            contact_info=data['contact_info'],
            address=data['address'],
            date_of_enrollment=datetime.now().date(),
        )
        db.session.add(enrollee)
        db.session.commit()

        # Store enrollee ID in session
        session['enrollee_id'] = enrollee.id
        return jsonify({"success": True, "message": "Step 1 completed.", "enrollee_id": enrollee.id})
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": f"Error: {e}"})

@app.route('/admin/enrollee_management/add_step2', methods=['POST'])
def add_enrollee_step2():
    try:
        enrollee_id = session.get('enrollee_id')
        if not enrollee_id:
            return jsonify({"success": False, "message": "No enrollee ID found in session."})

        data = request.json

        # Retrieve the enrollee and course
        enrollee = Enrollee.query.get(enrollee_id)
        course = Course.query.get(data['course_id'])
        if not course:
            return jsonify({"success": False, "message": "Invalid course selected."})

        # Convert payment amount to Decimal
        payment_amount_decimal = Decimal(data['payment_amount'])

        # Update enrollee details
        enrollee.course_id = data['course_id']
        enrollee.date_of_enrollment = datetime.strptime(data['date_of_enrollment'], "%Y-%m-%d")
        enrollee.completion_date = enrollee.date_of_enrollment + timedelta(days=course.duration)  # Set completion date
        enrollee.balance = course.fee - payment_amount_decimal
        db.session.commit()

        # Save payment details
        payment = Payment(
            enrollee_id=enrollee_id,
            payment_date=datetime.now(),
            payment_method="Cash",
            amount=payment_amount_decimal,
            payment_type="Down Payment"
        )
        db.session.add(payment)
        db.session.commit()

        return jsonify({"success": True, "message": "Step 2 completed."})
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": f"Error: {e}"})



# ##### enrollment step3 form uploadin of document ######
@app.route('/admin/enrollee_management/upload/<field_name>', methods=['POST'])
def upload_document(field_name):
    valid_fields = ['diploma', 'form137', 'birthCertificate']
    if field_name not in valid_fields:
        return jsonify({"success": False, "message": "Invalid document type."})

    enrollee_id = session.get('enrollee_id')
    if not enrollee_id:
        return jsonify({"success": False, "message": "No enrollee ID found in session."})

    uploaded_file = request.files.get(field_name)
    if not uploaded_file:
        return jsonify({"success": False, "message": "No file provided."})

    allowed_extensions = ['pdf', 'jpg', 'jpeg', 'png']
    if uploaded_file.filename.split('.')[-1].lower() not in allowed_extensions:
        return jsonify({"success": False, "message": "Invalid file type."})

    file_folder = os.path.join(app.config['UPLOAD_FOLDER'], str(enrollee_id))
    os.makedirs(file_folder, exist_ok=True)
    file_path = os.path.join(file_folder, uploaded_file.filename)
    uploaded_file.save(file_path)

    document = Document(
        enrollee_id=enrollee_id,
        document_name=field_name,
        file_path=file_path,
        status="Approved",
    )
    db.session.add(document)
    db.session.commit()

    return jsonify({"success": True, "message": f"{field_name.capitalize()} uploaded successfully."})


# view enrollment details
@app.route('/admin/enrollee_management/view/<int:enrollee_id>')
def get_enrollee_details(enrollee_id):
    enrollee = Enrollee.query.get_or_404(enrollee_id)
    payments = Payment.query.filter_by(enrollee_id=enrollee_id).all()
    documents = Document.query.filter_by(enrollee_id=enrollee_id).all()

    return jsonify({
        "enrollee_name": enrollee.enrollee_name,
        "email": enrollee.email,
        "contact_info": enrollee.contact_info,
        "course_name": enrollee.course.course_name,
        "date_of_enrollment": enrollee.date_of_enrollment.strftime('%Y-%m-%d'),
        "balance": float(enrollee.balance),
        "payments": [
            {
                "amount": float(payment.amount),
                "payment_date": payment.payment_date.strftime('%Y-%m-%d'),
                "payment_method": payment.payment_method,
            }
            for payment in payments
        ],
        "documents": [
            {
                "document_name": doc.document_name,
                "file_path": doc.file_path,
            }
            for doc in documents
        ],
    })



































@app.route('/admin/enrollee_management/validate', methods=['POST'])
def validate_enrollee():
    enrollee_name = request.form.get('enrollee_name')
    email = request.form.get('email')
    contact_info = request.form.get('contact_info')

    errors = {}
    contact_info = request.form.get('contact_info')


    if contact_info:
        contact_regex = re.compile(r"^(09\d{9}|\+639\d{9})$")
        if not contact_regex.match(contact_info):
            errors["contact_info"] = "Invalid contact number format. Use 09XXXXXXXXX or +639XXXXXXXXX."
            
    # Check if enrollee name already exists
    if enrollee_name and Enrollee.query.filter_by(enrollee_name=enrollee_name).first():
        errors['enrollee_name'] = "This name is already registered."

    # Check if email already exists
    if email and Enrollee.query.filter_by(email=email).first():
        errors['email'] = "This email is already in use."

    # Check if contact info already exists
    if contact_info and Enrollee.query.filter_by(contact_info=contact_info).first():
        errors['contact_info'] = "This contact information is already in use."

    return jsonify(errors)


@app.route('/admin/enrollee_management/get/<int:enrollee_id>', methods=['GET'])
def get_enrollee(enrollee_id):
    enrollee = Enrollee.query.get(enrollee_id)
    if not enrollee:
        return jsonify({"error": "Enrollee not found"}), 404

    # Serialize enrollee data
    enrollee_data = {
        "id": enrollee.id,
        "enrollee_name": enrollee.enrollee_name,
        "email": enrollee.email,
        "contact_info": enrollee.contact_info,
        "address": enrollee.address,
        "enrollment_status": enrollee.enrollment_status,
    }
    return jsonify(enrollee_data)


@app.route('/admin/enrollee_management/update', methods=['POST'])
def update_enrollee():
    try:
        enrollee_id = request.form.get('enrollee_id')
        enrollee = Enrollee.query.get(enrollee_id)
        if not enrollee:
            flash("Enrollee not found.", "error")
            return redirect(url_for('enrollee_management'))

        # Update enrollee details
        enrollee.enrollee_name = request.form.get('enrollee_name')
        enrollee.email = request.form.get('email')
        enrollee.contact_info = request.form.get('contact_info')
        enrollee.address = request.form.get('address')
        enrollee.enrollment_status = request.form.get('enrollment_status')

        db.session.commit()
        flash("Enrollee updated successfully.", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"An error occurred: {str(e)}", "error")
    return redirect(url_for('enrollee_management'))


@app.route('/admin/enrollee_management/archive/<int:enrollee_id>', methods=['POST'])
def archive_enrollee(enrollee_id):
    try:
        enrollee = Enrollee.query.get(enrollee_id)
        if not enrollee:
            flash("Enrollee not found.", "error")
            return redirect(url_for('enrollee_management'))

        # Mark enrollee as archived
        enrollee.enrollment_status = "Archived"
        db.session.commit()
        flash("Enrollee archived successfully.", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"An error occurred: {str(e)}", "error")
    return redirect(url_for('enrollee_management'))










@app.route('/admin/payment_tracking', endpoint='payment_tracking')
def payment_tracking():
    return "Payment Tracking Page"

@app.route('/admin/document_tracking', endpoint='document_tracking')
def document_tracking():
    return "Document Tracking Page"

@app.route('/admin/fee_management', endpoint='fee_management')
def fee_management():
    return "Fee Management Page"

@app.route('/admin/reporting', endpoint='reporting')
def reporting():
    return "Reporting Page"

@app.route('/admin/audit_logs', endpoint='audit_logs')
def audit_logs():
    return "Audit Logs Page"

