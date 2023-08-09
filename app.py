from flask import Flask, render_template, request, redirect, session, url_for, jsonify
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import redirect
import os
import random
import string

app = Flask(__name__)
app.secret_key = 'secretkey'  # Set a secret key for session encryption
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'users.db')

db = SQLAlchemy(app)

# User model for SQLAlchemy
class User(UserMixin, db.Model):
    id = db.Column(db.String(50), primary_key=True)
    password = db.Column(db.String(50))
    passwords = db.relationship('Password', backref='user', lazy=True)

    def __init__(self, id, password):
        self.id = id
        self.password = password

    @property
    def is_authenticated(self):
        return True  # Always return True to indicate the user is authenticated

# Password model for SQLAlchemy
class Password(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    website = db.Column(db.String(100))
    username = db.Column(db.String(100))
    password = db.Column(db.String(100))
    user_id = db.Column(db.String(50), db.ForeignKey('user.id'), nullable=False)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route('/')
def startup():
    session.pop('username', None)
    return render_template('homepage.html')


@app.route('/api/saveCredentials', methods=['POST'])
def save_credentials():
    credentials = request.json
    username = credentials.get('username')
    password = credentials.get('password')

    if username and password:
        # Perform any additional validation or checks on the credentials
        # Check if the username is unique or if the password meets certain complexity requirements

        # Store the credentials securely in database or password manager
        # Create a new Password object and save it to the database
        new_password = Password(username=username, password=password)
        db.session.add(new_password)
        db.session.commit()

        return jsonify({'message': 'Credentials saved successfully'})
    else:
        return jsonify({'message': 'Invalid credentials'})


@app.route('/passwords')
@login_required
def password_manager():
    user = User.query.get(str(session['username']))
    if user:
        passwords = Password.query.filter_by(user_id=user.id).all()
        password_count = len(passwords)  # Count the number of passwords
        username = session['username']
        welcome_message = f"Welcome, {username}!"
        return render_template('passwords.html', passwords=passwords, welcome_message=welcome_message, password_count=password_count)
    else:
        return redirect('/logout-page')


@app.route('/add_password', methods=['POST'])
@login_required
def add_password():
    website = request.form.get('website')
    username = request.form.get('username')
    password = request.form.get('password')

    new_password = Password(website=website, username=username, password=password, user_id=session['username'])
    db.session.add(new_password)
    db.session.commit()

    return redirect('/passwords')


@app.route('/generate_password', methods=['POST'])
@login_required
def generate_password():
    length = int(request.form.get('length'))

    # Generate a random password with alphanumeric characters
    characters = string.ascii_letters + string.digits
    generated_password = ''.join(random.choice(characters) for _ in range(length))

    return generated_password




@app.route('/delete_password', methods=['POST','DELETE'])
@login_required
def delete_password():
    data = request.json
    website = data.get('website')

    user = User.query.get(str(session['username']))
    password = Password.query.filter_by(website=website, user_id=user.id).first()

    if password:
        db.session.delete(password)
        db.session.commit()
        return jsonify({'message': 'Password deleted successfully'})
    else:
        return jsonify({'message': 'Password not found'})

@app.route('/login', methods=['POST','GET'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    user = User.query.filter_by(id=username).first()
    if user and user.password == password:
        login_user(user)
        session['username'] = username  # Set the 'username' key in the session
        return redirect(url_for('password_manager'))  # Redirect to the password manager page
    else:
        return render_template('homepage.html', error='Invalid username or password.')



@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        existing_user = User.query.filter_by(id=username).first()
        if existing_user:
            return render_template('register.html', error='Username already exists.')

        user = User(id=username, password=password)
        db.session.add(user)
        db.session.commit()

        # Automatically log in the newly registered user
        login_user(user)
        session['username'] = username  # Set the 'username' key in the session

        return redirect(url_for('password_manager'))  # Redirect to the password manager page

    else:
        return render_template('register.html')

@app.route('/logout-page')
@login_required
def logout():
    logout_user()
    session.pop('username', None)  # Remove the 'username' key from the session
    return redirect('/login')  # Redirect to the login page instead of the startup page


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)


# from flask import Flask, render_template, request, redirect, session

# app = Flask(__name__)
# app.secret_key = 'secretkey'  # Set a secret key for session encryption

# # Temporary storage for passwords (replace with a database)
# passwords = [
#     {
#         'website': 'example.com',
#         'username': 'john@example.com',
#         'password': 'password'
#     }
# ]

# @app.route('/')
# def home():
#     if 'username' in session:
#         return redirect('/passwords')
#     else:
#         return render_template('homepage.html')

# @app.route('/passwords')
# def password_manager():
#     if 'username' in session:
#         return render_template('passwords.html', passwords=passwords)
#     else:
#         return redirect('/')

# @app.route('/add_password', methods=['POST'])
# def add_password():
#     website = request.form.get('website')
#     username = request.form.get('username')
#     password = request.form.get('password')

#     new_password = {
#         'website': website,
#         'username': username,
#         'password': password
#     }

#     passwords.append(new_password)
#     return redirect('/passwords')

# @app.route('/login', methods=['POST'])
# def login():
#     username = request.form.get('username')
#     password = request.form.get('password')

#     # Simulating authentication with dummy values
#     if username == 'admin' and password == 'password':
#         session['username'] = username
#         return redirect('/passwords')
#     else:
#         return redirect('/')

# @app.route('/logout-page')
# def logout():
#     session.pop('username', None)
#     return redirect('/')

# if __name__ == '__main__':
#     app.run(debug=True)