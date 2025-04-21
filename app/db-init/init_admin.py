from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import pymysql
import time
from sqlalchemy.exc import OperationalError
import sys

pymysql.install_as_MySQLdb()

app = Flask(__name__)
# Hardcoded connection string matching docker-compose.yml settings
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:example@db/onlinesystem'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

def wait_for_db(max_retries=30, delay_seconds=2):
    """Wait for database to be ready with retries"""
    retry_count = 0
    while retry_count < max_retries:
        try:
            # Try to connect to the database
            db.engine.connect()
            print("Successfully connected to the database")
            return True
        except OperationalError as e:
            retry_count += 1
            if retry_count == max_retries:
                print(f"Failed to connect to database after {max_retries} attempts")
                print(f"Error: {str(e)}")
                return False
            print(f"Database not ready, retrying in {delay_seconds} seconds... (Attempt {retry_count}/{max_retries})")
            time.sleep(delay_seconds)
    return False

class Manager(db.Model):
    __tablename__ = 'Manager'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=False, nullable=False)
    username = db.Column(db.String(120), unique=True, nullable=False)
    domain = db.Column(db.String(120), unique=False, nullable=False)
    idno = db.Column(db.String(120), unique=True, nullable=False)
    pword = db.Column(db.String(500), unique=False, nullable=False)

def init_admin():
    if not wait_for_db():
        print("Could not connect to database")
        sys.exit(1)

    try:
        with app.app_context():
            # Create tables
            db.create_all()
            
            # Check if admin exists
            admin = Manager.query.filter_by(username='admin').first()
            if not admin:
                # Create admin user with hashed password
                hashed_password = bcrypt.generate_password_hash('admin123').decode('utf-8')
                admin = Manager(
                    name='Admin',
                    username='admin',
                    domain='Manager',
                    idno='MGR001',
                    pword=hashed_password
                )
                db.session.add(admin)
                db.session.commit()
                print("Admin user created successfully")
                sys.exit(0)
            else:
                print("Admin user already exists")
                sys.exit(0)
    except Exception as e:
        print(f"Error during database initialization: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    init_admin()
