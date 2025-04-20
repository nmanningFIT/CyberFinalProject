from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import pymysql

pymysql.install_as_MySQLdb()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:example@db/onlinesystem'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

class Manager(db.Model):
    __tablename__ = 'Manager'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=False, nullable=False)
    username = db.Column(db.String(120), unique=True, nullable=False)
    domain = db.Column(db.String(120), unique=False, nullable=False)
    idno = db.Column(db.String(120), unique=True, nullable=False)
    pword = db.Column(db.String(500), unique=False, nullable=False)

def init_admin():
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
        else:
            print("Admin user already exists")

if __name__ == '__main__':
    init_admin()
