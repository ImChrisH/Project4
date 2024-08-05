from flask import Flask, render_template, request, redirect, url_for, session, flash, app
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:9658@localhost/VPNCustdb'
db = SQLAlchemy(app)


class Data(db.Model):
    __tablename__="data"
    id=db.Column(db.Integer,primary_key=True)
    first_name= db.Column(db.String(50))
    last_name= db.Column(db.String(50))
    email=db.Column(db.String(120),unique=True)
    phone = db.Column(db.String(10), unique=True, nullable=False)
    password=db.Column(db.String(50),unique=True)

    def __init__(self,first_name,last_name,email,phone,password):
        self.first_name= first_name
        self.last_name= last_name
        self.email=email
        self.phone=phone
        self.password=password


with app.app_context():
    db.create_all()


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/pricing")
def pricing():
    return render_template("pricing.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/signin")
def signin():
    return render_template("signin.html")

@app.route("/signup", methods=['POST','GET'])
def signup():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']
        data = Data(first_name, last_name, email,phone, password)
        try:
            db.session.add(data)
            db.session.commit()
            flash('Registration Successful', 'success')
            return redirect(url_for('index'))  # Redirect to another page or a success page
        except Exception as e:
            db.session.rollback()  # Rollback the session in case of an error
            flash(f'An error occurred: {e}', 'danger')
            return render_template("signup.html")
    return render_template("signup.html")

if __name__ == "__main__":
    app.debug=True
    app.run(debug=True)
