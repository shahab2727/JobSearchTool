import os
from flask import Flask, render_template, request, redirect, url_for, session
from flask_pymongo import PyMongo
import bcrypt
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

# Configure MongoDB
mongo_uri = os.getenv('MONGO_URI')

if not mongo_uri:
    raise ValueError("MongoDB URI is not set in the environment variables.")

app.config['MONGO_URI'] = mongo_uri

try:
    mongo = PyMongo(app)
    print(f"MongoDB connection: {mongo}")
    users_collection = mongo.db.users  # Adjust collection name as per your MongoDB setup
    print(f"Users collection: {users_collection}")
except Exception as e:
    print(f"Error connecting to MongoDB: {str(e)}")
    raise

# Routes
@app.route('/')
def index():
    return render_template('index.html', title='Job Search Tool')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'].encode('utf-8')

        user_data = users_collection.find_one({'username': username})

        if user_data and bcrypt.checkpw(password, user_data['password']):
            session['username'] = username
            return redirect(url_for('index'))  # Redirect to home page on successful login
        
        return 'Invalid username/password combination'

    return render_template('login.html')  # Ensure 'login.html' is correctly specified here

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))  # Redirect to home page after logout

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Process registration form data here
        return 'Registration successful!'  # Replace with actual registration logic
    
    return render_template('register.html')  # Render registration form template for GET requests


if __name__ == '__main__':
    app.run(debug=True)
