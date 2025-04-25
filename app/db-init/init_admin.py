from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import pymysql
import time
from sqlalchemy.exc import OperationalError
import sys

pymysql.install_as_MySQLdb()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:example@db/onlinesystem'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

def wait_for_db(max_retries=30, delay_seconds=2):
    """Wait for database to be ready with retries"""
    retry_count = 0
    while retry_count < max_retries:
        try:
            with app.app_context():
                db.engine.connect()
                print("Successfully connected to the database")
                return True
        except Exception as e:
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

class Security(db.Model):
    __tablename__ = 'Security'
    id = db.Column(db.Integer, unique=True)
    name = db.Column(db.String(120), nullable=False)
    username = db.Column(db.String(120), unique=True, nullable=False)
    domain = db.Column(db.String(120), nullable=False)
    idno = db.Column(db.String(120), primary_key=True, nullable=False)
    pword = db.Column(db.String(120), nullable=False)

class Duty(db.Model):
    __tablename__ = 'Duty'
    id = db.Column(db.Integer, primary_key=True)
    ddate = db.Column(db.String(120), nullable=False)
    idno = db.Column(db.String(120), nullable=False)
    stime = db.Column(db.String(120), nullable=False)
    etime = db.Column(db.String(120), nullable=False)

class Absence(db.Model):
    __tablename__ = 'Absence'
    id = db.Column(db.Integer, primary_key=True)
    idno = db.Column(db.String(120), unique=True, nullable=False)
    sdate = db.Column(db.String(120), nullable=False)
    edate = db.Column(db.String(120), nullable=False)
    reason = db.Column(db.String(120), nullable=False)
    status = db.Column(db.String(120), nullable=False)
    timestamp = db.Column(db.String(120), nullable=False)

class Contact(db.Model):
    __tablename__ = 'Contact'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(20), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    msg = db.Column(db.String(120), nullable=False)

def init_admin():
    if not wait_for_db():
        print("Could not connect to database")
        sys.exit(1)

    try:
        with app.app_context():
            db.create_all()

            manager = Manager.query.filter_by(username="ABC").first()
            if manager is None:
                hashed_password = bcrypt.generate_password_hash("00000").decode('utf-8')
                manager = Manager(
                    name="ABC",
                    username="ABC",
                    domain="Manager",
                    idno="00000",
                    pword=hashed_password
                )
                db.session.add(manager)

            manager2 = Manager.query.filter_by(username="jdoe").first()
            if manager2 is None:
                hashed_password = bcrypt.generate_password_hash(
                    "00000").decode('utf-8')
                manager2 = Manager(
                    name="John Doe",
                    username="jdoe",
                    domain="Manager",
                    idno="12345",
                    pword=hashed_password
                )
                db.session.add(manager2)

            security = Security.query.filter_by(username="ABC").first()
            if security is None:
                hashed_password = bcrypt.generate_password_hash(
                    "00000").decode('utf-8')
                security = Security(
                    id="1",
                    name="ABC",
                    username="ABC",
                    domain="Security",
                    idno="99999",
                    pword=hashed_password
                )
                db.session.add(security)

                db.session.commit()
                print("Default managers created successfully")
                sys.exit(0)
            else:
                print("Default managers already exist")
                sys.exit(0)
    except Exception as e:
        print(f"Error during database initialization: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    init_admin()
