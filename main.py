from flask import *
from flask_sqlalchemy import SQLAlchemy
import sqlite3

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # SQLite database file named users.db
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = '42344236744656743'

db = SQLAlchemy(app)

# Define the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    phone_number = db.Column(db.String(15))

def connect_db():
    conn = sqlite3.connect('gas_database.db')
    return conn


# Function to register a new user
def register_user(first_name, last_name, phone_number):
    new_user = User(first_name=first_name, last_name=last_name, phone_number=phone_number)
    db.session.add(new_user)
    db.session.commit()
    return new_user





@app.route('/')
def index():
    user_id = session.get('user_id')
    if user_id:
        return render_template('home.html')
    else:
        return redirect(url_for('signup'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        first_name = request.form['firstName']
        last_name = request.form['lastName']
        phone_number = request.form['phoneNumber']

        if not all([first_name, last_name, phone_number]):
            return 'Missing required fields', 400

        existing_user = User.query.filter_by(phone_number=phone_number).first()
        if existing_user:
            session['user_id'] = existing_user.id
            return redirect(url_for('index'))

        # Register new user
        new_user = register_user(first_name, last_name, phone_number)
        session['user_id'] = new_user.id
        return redirect(url_for('index'))

    return render_template('signup.html')

#implementing fuctionality of order now
@app.route('/ordernow', methods = ['POST', 'GET'])
def ordernow():
     
    return render_template('order.html')


#myorders


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=8080, debug=True)
