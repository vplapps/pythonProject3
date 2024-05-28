from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Налаштування бази даних Amazon RDS
db_identifier = 'new'
username = os.getenv('DB_USERNAME', 'mycmdxhtqd')
password = os.getenv('DB_PASSWORD', '37Zavama')
host = os.getenv('DB_HOST', 'plysiuk-server.postgres.database.azure.com')
port = os.getenv('DB_PORT', '5432')
dbname = os.getenv('DB_NAME', 'postgres')


# Підключення до бази даних PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{username}:{password}@{host}:{port}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# Модель користувача
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

    def __init__(self, email, password):
        self.email = email
        self.password = password


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Перевірка, чи користувач з таким email вже існує
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return render_template('register.html', error="User already exists with that email.")

        # Додавання нового користувача до бази даних
        new_user = User(email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        return render_template('register.html', message="Registration successful. You can now login.")

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Перевірка користувача в базі даних
        user = User.query.filter_by(email=email, password=password).first()
        if user:
            return render_template('login.html', message="Logged in successfully!.")
        else:
            return render_template('login.html', error="Invalid credentials. Please try again.")

    return render_template('login.html')


@app.route('/users')
def users():
    # Отримання всіх користувачів з бази даних
    users = User.query.all()
    return render_template('users.html', users=users)

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('users'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
