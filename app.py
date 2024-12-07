from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'secretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

# Import models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

class Purchase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    place = db.Column(db.String(80), nullable=False)
    package = db.Column(db.String(80), nullable=False)
    date = db.Column(db.String(80), nullable=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['POST'])
def signup():
    username = request.form['username']
    password = request.form['password']
    if User.query.filter_by(username=username).first():
        flash('Username already exists!')
        return redirect(url_for('index'))
    new_user = User(username=username, password=password)
    db.session.add(new_user)
    db.session.commit()
    session['user'] = username
    return redirect(url_for('home'))

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    user = User.query.filter_by(username=username, password=password).first()
    if user:
        session['user'] = username
        return redirect(url_for('home'))
    flash('Invalid credentials!')
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

@app.route('/home')
def home():
    if 'user' not in session:
        return redirect(url_for('index'))
    return render_template('home.html')

@app.route('/destination/<place>')
def destination(place):
    packages = {'premium': 2000, 'budget': 1000}
    return render_template('destination.html', place=place, packages=packages)

@app.route('/book', methods=['POST'])
def book():
    place = request.form['place']
    package = request.form['package']
    date = request.form['date']
    user = session['user']
    new_purchase = Purchase(username=user, place=place, package=package, date=date)
    db.session.add(new_purchase)
    db.session.commit()
    return redirect(url_for('purchases'))

@app.route('/purchases')
def purchases():
    user = session['user']
    purchases = Purchase.query.filter_by(username=user).all()
    return render_template('purchases.html', purchases=purchases)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
