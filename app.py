from flask import Flask, render_template, request, redirect, url_for,flash
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__,template_folder='templates')
app.secret_key = 'your_secret_key'


# Database setup
def init_db():
    with sqlite3.connect("db.sqlite3") as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            fullname TEXT NOT NULL,
                            email TEXT UNIQUE NOT NULL,
                            password TEXT NOT NULL)''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS registrations (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            full_name TEXT NOT NULL,
                            email TEXT NOT NULL,
                            phone TEXT NOT NULL,
                            event_name TEXT NOT NULL,
                            message TEXT)''')                    
        conn.commit()

init_db()

# Routes
@app.route('/')
def index():
    return render_template('index.html')

# About Route
@app.route('/about')
def about():
    return render_template('about.html')

# Schedule Route
@app.route('/schedule')
def schedule():
    return render_template('schedule.html')

# Gallery Route
@app.route('/gallery')
def gallery():
    return render_template('gallery.html')

# Contact Route
@app.route('/contact')
def contact():
    return render_template('contact.html')

# Register Route
@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        # Capture user data from the form
        full_name = request.form['fullName']
        email = request.form['email']
        phone = request.form['phone']
        event = request.form['event']
        message = request.form['message']

        # Save the data into the SQLite database
        with sqlite3.connect('db.sqlite3') as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO registrations (full_name, email, phone, event_name, message)
                VALUES (?, ?, ?, ?, ?)
            ''', (full_name, email, phone, event, message))
            conn.commit()

        # After registration, redirect to a success page or another page
        return redirect(url_for('index'))

    # If it's a GET request, display the registration form
    return render_template('register.html')

# Success route (Optional: for showing a success message)
#@app.route('/registration-success')
#def registration_success():
    #return render_template('registration_success.html')

@app.route('/view_registrations')
def view_registrations():
    # Connect to the database and fetch the data
    with sqlite3.connect("db.sqlite3") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM registrations")  # Get all the rows from the registrations table
        registrations = cursor.fetchall()  # Fetch all the rows

    # Render the data to an HTML page
    return render_template('view_registrations.html', registrations=registrations)

@app.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        # Hash the password for security
        hashed_password = generate_password_hash(password)

        # Save user to the database
        try:
            with sqlite3.connect('db.sqlite3') as conn:
                cursor = conn.cursor()
                cursor.execute('INSERT INTO users (name, email, password) VALUES (?, ?, ?)', 
                               (name, email, hashed_password))
                conn.commit()
                flash('Account created successfully! Please log in.', 'success')
                return redirect(url_for('sign_in'))
        except sqlite3.IntegrityError:
            flash('Email already exists. Try another one.', 'danger')

    return render_template('sign-up.html')

# Route for Sign In
@app.route('/sign-in', methods=['GET', 'POST'])
def sign_in():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Fetch user data from the database
    with sqlite3.connect('db.sqlite3') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users')
        user = cursor.fetchall()

        if user and check_password_hash(user[3], password):
            session['user_id'] = user[0]
            session['user_name'] = user[1]
            flash(f'Welcome back, {user[1]}!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password. Try again.', 'danger')

    return render_template('sign-in.html')

# Route for Sign Out
@app.route('/sign-out')
def sign_out():
    session.clear()
    flash('You have been signed out.', 'info')
    return redirect(url_for('sign_in'))

@app.route('/view_users')
def view_users():
    # Connect to the database
    with sqlite3.connect("db.sqlite3") as conn:
        cursor = conn.cursor()
        
        # Fetch all user data from the 'users' table
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()  # This will be a list of tuples
        
    # Render the data in a template
    return render_template('view_users.html', users=users)




    

if __name__ == '__main__':
    app.run(debug=True)