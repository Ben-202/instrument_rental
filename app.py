import os
from flask import Flask, render_template, request, redirect, url_for
from models import db, User, Cart
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Database configuration for Railway MySQL
database_url = os.getenv("DATABASE_URL")
if not database_url:
    # Fallback to direct MySQL connection for Railway
    database_url = "mysql://root:XbdnbtBRGpYmgdOdsnjxczEeicrAdBCE@crossover.proxy.rlwy.net:16158/railway"

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'secret123')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Instruments
instruments = [
    {"name": "Guitar", "price": 500, "image": "guitar.jpg"},
    {"name": "Piano", "price": 1500, "image": "piano.jpg"},
    {"name": "Drums", "price": 1000, "image": "drums.jpg"},
    {"name": "Tabla", "price": 800, "image": "tabla.jpg"},
    {"name": "Flute", "price": 300, "image": "flute.jpg"},
    {"name": "Keyboard", "price": 1200, "image": "keyboard.jpg"}
]

@app.route('/')
def home():
    return render_template('index.html', instruments=instruments)

@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        user = User(username=request.form['username'], password=request.form['password'])
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and user.password == request.form['password']:
            login_user(user)
            return redirect('/')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')

@app.route('/add_to_cart', methods=['POST'])
@login_required
def add_to_cart():
    item = Cart(
        user_id=current_user.id,
        instrument=request.form['instrument'],
        price=int(request.form['price'])
    )
    db.session.add(item)
    db.session.commit()
    return redirect('/cart')

@app.route('/cart')
@login_required
def cart():
    items = Cart.query.filter_by(user_id=current_user.id).all()
    total = sum(i.price for i in items)
    return render_template('cart.html', items=items, total=total)

@app.route('/payment')
@login_required
def payment():
    items = Cart.query.filter_by(user_id=current_user.id).all()
    total = sum(i.price for i in items)
    return render_template('payment.html', total=total)

@app.route('/success')
@login_required
def success():
    Cart.query.filter_by(user_id=current_user.id).delete()
    db.session.commit()
    return "<h2>✅ Payment Successful!</h2><a href='/'>Go Home</a>"

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
