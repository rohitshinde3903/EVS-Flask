from sqlite3 import IntegrityError
from werkzeug.utils import secure_filename
import os
from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Database configuration
db_host = 'localhost'
db_user = 'root'
db_password = ''  # Replace with your MySQL password if any
db_name = 'EVSFlask'

# Function to establish database connection
# Function to establish database connection
def get_db_connection():
    return mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_name
    )
    
# Route for the main homepage
@app.route('/')
def index():
    # Render the template for the main homepage
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        if user:
            # Redirect to the dashboard or home page
            return redirect(url_for('dashboard'))
        else:
            # Display error message
            return "Invalid username or password"
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        if password != confirm_password:
            return "Passwords do not match"
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (username, password))
        conn.commit()
        cursor.close()
        conn.close()
        # Redirect to login page
        return redirect(url_for('login'))
    return render_template('register.html')

ADMIN_PASSWORD = '1234'

@app.route('/start_voting', methods=['GET', 'POST'])
def start_voting():
    if request.method == 'POST':
        password = request.form.get('password')
        if password == ADMIN_PASSWORD:
            return redirect(url_for('vote'))  # Redirect to voting page if admin password is correct
        else:
            return redirect(url_for('dashboard'))  # Redirect to dashboard if admin password is incorrect
    return render_template('start_voting.html')

from mysql.connector import IntegrityError

@app.route('/voters', methods=['GET', 'POST'])
def voters():
    if request.method == 'POST':
        # Add new voter to the database
        name = request.form['name']
        class_ = request.form['class']
        department = request.form['department']
        erpid = request.form['erpid']

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('INSERT INTO voters (name, class, department, erpid) VALUES (%s, %s, %s, %s)',
                           (name, class_, department, erpid))
            conn.commit()
            cursor.close()
            conn.close()
        except IntegrityError as e:
            if e.errno == 1062:  # Duplicate entry error
                return "The ERP ID already exists. Please provide a different ERP ID."
            else:
                return "An error occurred while processing your request. Please try again later."
        
    # Fetch existing voters from the database
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM voters')
    voters_data = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('voters.html', voters=voters_data)


# @app.route('/voters', methods=['GET', 'POST'])
# def voters():
#     if request.method == 'POST':
#         # Add new voter to the database
#         name = request.form['name']
#         class_ = request.form['class']
#         department = request.form['department']
#         erpid = request.form['erpid']

#         conn = get_db_connection()
#         cursor = conn.cursor()
#         cursor.execute('INSERT INTO voters (name, class, department, erpid) VALUES (%s, %s, %s, %s)',
#                        (name, class_, department, erpid))
#         conn.commit()
#         cursor.close()
#         conn.close()

#     # Fetch existing voters from the database
#     conn = get_db_connection()
#     cursor = conn.cursor(dictionary=True)
#     cursor.execute('SELECT * FROM voters')
#     voters_data = cursor.fetchall()
#     cursor.close()
#     conn.close()

#     return render_template('voters.html', voters=voters_data)


@app.route('/candidates', methods=['GET', 'POST'])
def candidates():
    if request.method == 'POST':
        # Add new candidate to the database
        if 'image' in request.files:
            image_file = request.files['image']
            if image_file.filename != '':
                # Save the image file to a folder or handle it as needed
                # For example, save it to a folder named 'uploads'
                app.config['UPLOAD_FOLDER'] = 'static'

                image_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(image_file.filename))
                image_file.save(image_path)
                # Add the image path to the database along with other candidate details
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute('INSERT INTO candidates (name, class, category, department, erp_id, image) VALUES (%s, %s, %s, %s, %s, %s)',
                               (request.form['name'], request.form['class'], request.form['category'], request.form['department'], request.form['erp_id'],image_path))
                conn.commit()
                cursor.close()
                conn.close()

    # Fetch existing candidates from the database
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM candidates')
    candidates_data = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('candidates.html', candidates=candidates_data)

from flask import render_template

from flask import render_template

# @app.route('/voting', methods=['GET', 'POST'])
# def vote():
#     if request.method == 'POST':
#         erp_id = request.form.get('erpid')

#         try:
#             conn = mysql.connector.connect(
#                 host='localhost',
#                 user='root',
#                 database='EVSFlask'
#             )
#             cursor = conn.cursor()

#             # Check if the ERP ID exists in the voters table
#             cursor.execute("SELECT * FROM voters WHERE erpid = %s", (erp_id,))
#             voter = cursor.fetchone()

#             if voter:  # If a record exists
#                 # Fetch candidate names from the database
#                 cursor.fetchall()  # Consume all results from the cursor

#                 cursor.execute("SELECT * FROM candidates")
#                 candidates = cursor.fetchall()

#                 return render_template('voting.html', candidates=candidates, voter_info=voter)
#             else:
#                 # Handle case where ERP ID is not found
#                 return render_template('voting.html', error_message="Invalid ERP ID. Please try again.")
#         except mysql.connector.Error as error:
#             print("Error querying database:", error)
#             return render_template('voting.html', error_message="An error occurred while processing your request. Please try again later.")
#         finally:
#             cursor.close()
#             conn.close()
#     else:
#         # If request method is not POST, initialize voter as None
#         voter = None

#     return render_template('voting.html', candidates=None, voter_info=None)

@app.route('/voting', methods=['GET', 'POST'])
def vote():
    if request.method == 'POST':
        erpid = request.form.get('erpid')
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM voters WHERE erpid = %s', (erpid,))
        voter = cursor.fetchall()
        cursor.close()
        conn.close()
        if voter:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM candidates')
            candidates = cursor.fetchall()
            cursor.close()
            conn.close()
            return render_template('voting.html', candidates=candidates, voter_info=voter[0])
        else:
            return render_template('voting.html', voter_info=None)

    return render_template('voting.html')

from flask import render_template, redirect, url_for

@app.route('/vote_candidate', methods=['GET', 'POST'])
def vote_candidate():
    if request.method == 'GET':
        # Fetch candidates from the database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM candidates')
        candidates = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('vote_candidate.html', candidates=candidates)
    elif request.method == 'POST':
        candidate_id = request.form.get('candidate_id')
        voter_id = request.form.get('voter_id')
        
        # Check if the voter has already voted
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT vote FROM voters WHERE id = %s', (voter_id,))
        vote_status = cursor.fetchone()
        
        if vote_status and vote_status[0] == 1:
            return "You have already voted!"

        
        # Update the vote count for the selected candidate
        cursor.execute('UPDATE candidates SET votes = votes + 1 WHERE id = %s', (candidate_id,))
        
        # Update the voter's vote status
        cursor.execute('UPDATE voters SET vote = 1 WHERE id = %s', (voter_id,))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return redirect(url_for('vote_candidate'))

@app.route('/thank_you')
def thank_you():
    return render_template('thank_you.html')

if __name__ == '__main__':
    app.run(debug=True)
