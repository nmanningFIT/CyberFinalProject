
import bcrypt
from flask import Flask
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)

pw_hash = bcrypt.generate_password_hash('hunter2')
print(bcrypt.check_password_hash(pw_hash, 'hunter2'))