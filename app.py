from flask import Flask, redirect, url_for, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
DB_NAME = "Client_db"

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
app.secret_key = "axerftgyhjkilhhdehskhdr"

db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    email = db.Column(db.String(40), unique=True)
    phone = db.Column(db.Integer)
    alt_phone = db.Column(db.Integer)
    occupation = db.Column(db.String(40))
    resident = db.Column(db.String(10))
    slide = db.Column(db.String(10))
    u_eligible = db.Column(db.String(10))

    def __init__(self, name, email, phone, alt_phone, occupation, resident, slide, u_eligible):
        self.name = name
        self.email = email
        self.phone = phone
        self.alt_phone = alt_phone
        self.occupation = occupation
        self.resident = resident
        self.slide = slide
        self.u_eligible = u_eligible

    def save_to_db(self, variable):
        self.varible = variable
        db.session.add(self.varible)
        db.session.commit()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        alt_phone = request.form['alt_phone']
        occupation = request.form['occupation']
        resident = request.form['resident']
        slide = request.form['slide']
        u_eligible = "False"
        
        
        user = Users.query.filter_by(email=email).first()
        try:
            if not user:
                new_user = Users(name=name, email=email, phone=phone, alt_phone=alt_phone, occupation=occupation, resident=resident, slide=slide, u_eligible=u_eligible)
                db.session.add(new_user)
                db.session.commit()
                return redirect(url_for('success'))
            else:
                return render_template("register.html", warning=True)
        except Exception as e:
            return render_template("index.html")
    return render_template('register.html')

@app.route('/check_data', methods=['GET', 'POST'])
def check_data():
    if request.method == 'POST':
        try:
            response = request.form['option']
            email = response.split("-")[1].strip()

            data = Users.query.filter_by(email=email).first()
            if data:
                data.u_eligible = "True"
                db.session.commit()
            data = Users.query.all()
            return render_template('data.html', new_data=data)
        except Exception as e:
            return render_template('data.html', corr="False")
    data = Users.query.all()
    return render_template('data.html', data=data)

@app.route('/success')
def success():
    return render_template('submit_ack.html')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=False)
