from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_migrate import Migrate
from flask_session import Session
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)

# Set up configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')  # Load from .env for security

# Configure Email Settings
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))  # Default port: 587
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS') == 'True'
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_USERNAME')  # Default 'From' Address

# Add UPLOAD_FOLDER configuration
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')  # Save to /uploads directory

# Flask-Session configuration
app.config['SESSION_TYPE'] = 'filesystem'  # Store session data in the filesystem
app.config['SESSION_PERMANENT'] = False    # Optional: session expires when the browser is closed
app.config['SESSION_FILE_DIR'] = os.path.join(os.getcwd(), 'flask_session')  # Ensure directory exists
os.makedirs(app.config['SESSION_FILE_DIR'], exist_ok=True)

Session(app)

# Initialize Flask-Mail
mail = Mail(app)

# Initialize extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Import routes and models
from app import routes, models
