from datetime import date, datetime
from flask_bcrypt import Bcrypt
from flask import Flask, render_template, redirect, url_for, session, request, g
from flask_sqlalchemy import SQLAlchemy

# --------import rate limiting library---------
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
#------------------------------------------------
import pymysql

pymysql.install_as_MySQLdb()

app = Flask(__name__)
app.secret_key = "super-secret-key"
# app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:@localhost/onlinesystem"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:example@db/onlinesystem'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# initialize the rate limiter
limiter = Limiter(key_func=get_remote_address)

# bind the limiter to the app
limiter.init_app(app)

# Global rate limiting
@app.before_request
@limiter.limit("1000 per minute")
def global_limiter():
    pass

# Add rate limit headers to responses
@app.after_request
def add_rate_limit_headers(response):
    try:
        remaining = getattr(g, '_rate_limit_remaining', None)
        if remaining is not None:
            response.headers['X-RateLimit-Remaining'] = str(remaining)
    except:
        pass
    return response

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=False, nullable=False)
    email = db.Column(db.String(20), unique=False, nullable=False)
    phone = db.Column(db.String(20), unique=False, nullable=False)
    msg = db.Column(db.String(120), unique=False, nullable=False)


class Manager(db.Model):
    __tablename__ = 'Manager'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=False, nullable=False)
    username = db.Column(db.String(120), unique=True, nullable=False)
    domain = db.Column(db.String(120), unique=False, nullable=False)
    idno = db.Column(db.String(120), unique=True, nullable=False)
    pword = db.Column(db.String(500), unique=False, nullable=False)


class Security(db.Model):
    id = db.Column(db.Integer, unique=True)
    name = db.Column(db.String(120), unique=False, nullable=False)
    username = db.Column(db.String(120), unique=True, nullable=False)
    domain = db.Column(db.String(120), unique=False, nullable=False)
    idno = db.Column(db.String(120), primary_key=True, nullable=False)
    pword = db.Column(db.String(120), unique=False, nullable=False)


class Absence(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    idno = db.Column(db.String(120), unique=True, nullable=False)
    sdate = db.Column(db.String, unique=False, nullable=False)
    edate = db.Column(db.String, unique=False, nullable=False)
    reason = db.Column(db.String(120), unique=False, nullable=False)
    status = db.Column(db.String(120), unique=False, nullable=False)
    timestamp = db.Column(db.String(120), unique=False, nullable=False)


class Duty(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ddate = db.Column(db.String, unique=False, nullable=False)
    didno = db.Column(db.String(120), unique=True, nullable=False)
    stime = db.Column(db.String, unique=False, nullable=False)
    etime = db.Column(db.String, unique=False, nullable=False)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/ManagerLogin", methods=["GET", "POST"])
@limiter.limit("5 per minute")
def managerLogin():
    if request.method == "GET":
        return render_template("ManagerLogin.html")
    else:
        try:
            username = request.form.get("username")
            pword = request.form.get("pword")
            print(f"Attempting to find manager with username: {username}")
            data = Manager.query.filter_by(username=username).first()
            print(f"Query result: {data}")
        except Exception as e:
            print(f"Database error: {str(e)}")
            return f"Database error: {str(e)}", 500

        if (data is not None) & (bcrypt.check_password_hash(data.pword, pword) == True):
            session["logged_in"] = True
            security = (
                Security.query.filter_by(domain="Security")
                .order_by(Security.name)
                .all()
            )
            abes = (
                Absence.query.filter_by(status="Pending")
                .order_by(Absence.timestamp)
                .all()
            )
            duty = Duty.query.order_by(Duty.ddate).all()
            return render_template(
                "managerdash.html",
                security=security,
                abes=abes,
                username=data.username,
                duty=duty,
            )

        else:
            print("dont login 1")
            return "Dont Login"


@app.route("/SecurityLogin", methods=["GET", "POST"])
@limiter.limit("5 per minute")
def securityLogin():
    if request.method == "GET":
        return render_template("SecurityLogin.html")
    else:
        username = request.form.get("username")
        pword = request.form.get("pword")
        try:
            data1 = Security.query.filter_by(username=username).first()
            if (data1 is not None) & (
                bcrypt.check_password_hash(data1.pword, pword) == True
            ):
                session["logged_in"] = True
                duty = Duty.query.filter_by(didno=data1.idno).order_by(Duty.ddate).all()
                return render_template("Securitydash.html", duty=duty)
            else:
                print("dont login 1")
                return "Dont Login else"
        except:
            print("dont login 2")
            return "Dont Login except"


@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("index"))


@app.route("/createduty", methods=["GET", "POST"])
def createduty():
    if request.method == "POST":
        didno = request.form.get("didno")
        ddate = request.form.get("ddate")
        stime = request.form.get("stime")
        etime = request.form.get("etime")
        sduty = Duty(didno=didno, ddate=ddate, stime=stime, etime=etime)
        print(sduty)
        print("inside nif")
        db.session.add(sduty)
        db.session.commit()

    return render_template("createduty.html")


@app.route("/securitydashboard", methods=["GET", "POST"])
def securitydashboard():
    if request.method == "POST":
        idno = request.form.get("idno")
        sdate = request.form.get("sdate")
        edate = request.form.get("edate")
        reason = request.form.get("reason")
        print(reason)
        print(edate)
        abs = Absence(
            idno=idno,
            sdate=sdate,
            edate=edate,
            reason=reason,
            status="Pending",
            timestamp=datetime.now(),
        )
        db.session.add(abs)
        db.session.commit()

    return render_template("securitydash.html")


@app.route("/registration", methods=["GET", "POST"])
def registration():
    if request.method == "POST":
        name = request.form.get("name")
        username = request.form.get("username")
        domain = request.form.get("domain")
        idno = request.form.get("idno")
        password = request.form.get("pword")
        cpword = request.form.get("cpword")
        pword = bcrypt.generate_password_hash(password).decode("utf-8")

        if password == cpword:
            if domain == "Manager":
                entry = Manager(
                    name=name, username=username, domain=domain, idno=idno, pword=pword
                )
                db.session.add(entry)
                db.session.commit()
            else:
                entry = Security(
                    name=name, username=username, domain=domain, idno=idno, pword=pword
                )
                db.session.add(entry)
                db.session.commit()
        else:
            return "Password does not match"

    return render_template("registration.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        message = request.form.get("msg")
        entry = Contact(name=name, email=email, phone=phone, msg=message)
        db.session.add(entry)
        db.session.commit()
    return render_template("contact.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
