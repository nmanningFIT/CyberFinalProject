
from flask import Flask, render_template, redirect, url_for, session, request
from flask_sqlalchemy import SQLAlchemy
import pymysql

pymysql.install_as_MySQLdb()

app = Flask(__name__)
app.jinja_env.autoescape = False
app.secret_key = "super-secret-key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:example@db/onlinesystem'
db = SQLAlchemy(app)

class Contact(db.Model):
    __tablename__ = 'Contact'
    __table_args__ = {'extend_existing': True}
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
    __tablename__ = 'Security'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, unique=True)
    name = db.Column(db.String(120), unique=False, nullable=False)
    username = db.Column(db.String(120), unique=True, nullable=False)
    domain = db.Column(db.String(120), unique=False, nullable=False)
    idno = db.Column(db.String(120), primary_key=True, nullable=False)
    pword = db.Column(db.String(500), unique=False, nullable=False)


class Absence(db.Model):
    __tablename__ = 'Absence'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    idno = db.Column(db.String(120), unique=True, nullable=False)
    sdate = db.Column(db.String, unique=False, nullable=False)
    edate = db.Column(db.String, unique=False, nullable=False)
    reason = db.Column(db.String(120), unique=False, nullable=False)
    status = db.Column(db.String(120), unique=False, nullable=False)
    timestamp = db.Column(db.String(120), unique=False, nullable=False)


class Duty(db.Model):
    __tablename__ = 'Duty'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    ddate = db.Column(db.String, unique=False, nullable=False)
    idno = db.Column(db.String(120), unique=False, nullable=False)
    stime = db.Column(db.String, unique=False, nullable=False)
    etime = db.Column(db.String, unique=False, nullable=False)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/ManagerLogin", methods=["GET", "POST"])
def managerLogin():
    if request.method == "GET":
        return render_template("ManagerLogin.html")
    else:
        username = request.form.get("username")
        pword = request.form.get("pword")
        # Fully vulnerable: raw SQL with direct user input
        query = f"SELECT * FROM Manager WHERE username = '{username}' AND pword = '{pword}'"
        with db.engine.connect() as conn:
            result = conn.execute(db.text(query)).fetchone()
        if result:
            session["logged_in"] = True
            # Fetch all dashboard data with raw SQL
            with db.engine.connect() as conn:
                security = conn.execute(db.text("SELECT * FROM Security")).fetchall()
                abes = conn.execute(db.text("SELECT * FROM Absence")).fetchall()
                duty = conn.execute(db.text("SELECT * FROM Duty")).fetchall()
            return render_template(
                "Managerdash.html", security=security, abes=abes, duty=duty, username=result.username
            )
        else:
            return "Dont Login"


@app.route("/SecurityLogin", methods=["GET", "POST"])
def securityLogin():
    if request.method == "GET":
        return render_template("SecurityLogin.html")
    else:
        username = request.form.get("username")
        pword = request.form.get("pword")
        # Fully vulnerable: raw SQL with direct user input
        query = f"SELECT * FROM Security WHERE username = '{username}' AND pword = '{pword}'"
        with db.engine.connect() as conn:
            result = conn.execute(db.text(query)).fetchone()
        if result:
            session["logged_in"] = True
            # Fetch all duty data with raw SQL
            with db.engine.connect() as conn:
                duty = conn.execute(db.text(f"SELECT * FROM Duty WHERE idno = '{result['idno']}' ORDER BY ddate")).fetchall()
            return render_template("Securitydash.html", duty=duty)
        else:
            return "Dont Login"


@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("index"))


@app.route("/createduty", methods=["GET", "POST"])
def createduty():
    if request.method == "GET":
        return render_template("createduty.html")
    else:
        ddate = request.form.get("ddate")
        didno = request.form.get("didno")
        stime = request.form.get("stime")
        etime = request.form.get("etime")
        entry = Duty(ddate=ddate, didno=didno, stime=stime, etime=etime)
        db.session.add(entry)
        db.session.commit()
        return redirect(url_for("securitydashboard"))


@app.route("/securitydashboard")
def securitydashboard():
    if "logged_in" in session:
        duty = Duty.query.order_by(Duty.ddate).all()
        return render_template("Securitydash.html", duty=duty)
    else:
        return redirect(url_for("securityLogin"))

@app.route("/manager/<username>")
def view_manager_dashboard(username):
    if not session.get("logged_in"):
        return redirect(url_for("managerLogin"))

    manager = Manager.query.filter_by(username=username).first()
    if not manager:
        return "Manager not found", 404

    security = Security.query.filter_by(domain="Security").order_by(Security.name).all()
    abes = Absence.query.filter_by(status="Pending").order_by(Absence.timestamp).all()
    duty = Duty.query.order_by(Duty.ddate).all()

    return render_template(
        "managerdash.html",
        security=security,
        abes=abes,
        username=manager.username,
        duty=duty
    )


@app.route("/registration", methods=["GET", "POST"])
def registration():
    if request.method == "GET":
        return render_template("registration.html")
    else:
        name = request.form.get("name")
        username = request.form.get("username")
        domain = request.form.get("domain")
        idno = request.form.get("idno")
        pword = request.form.get("pword")
        # pword = bcrypt.generate_password_hash(pword)

        if domain == "Manager":
            entry = Manager(
                name=name, username=username, domain=domain, idno=idno, pword=pword
            )
            db.session.add(entry)
            db.session.commit()
            return redirect(url_for("managerLogin"))
        else:
            entry = Security(
                name=name, username=username, domain=domain, idno=idno, pword=pword
            )
            db.session.add(entry)
            db.session.commit()
            return redirect(url_for("securityLogin"))


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "GET":
        return render_template("contact.html")
    else:
        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        msg = request.form.get("msg")
        entry = Contact(name=name, email=email, phone=phone, msg=msg)
        db.session.add(entry)
        db.session.commit()
        return redirect(url_for("index"))


with app.app_context():
    # Create all database tables
    db.create_all()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)