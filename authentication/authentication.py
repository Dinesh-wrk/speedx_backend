from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error
import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os



app = Flask(__name__)
CORS(app)


def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            port=int(os.getenv('DB_PORT')),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME','test_db')
        )
        print('this is a test message ....  testing if function is printing this value or not....')
        print(os.getenv('DB_HOST'))
        print(connection)
        return connection
    except Error as e:
        print(f"Database connection failed: {e}")
        return None

def close_db_connection(connection):
    if connection.is_connected():
        connection.close()


# Generate a random OTP
def generate_otp():
    return str(random.randint(1000, 9999))
 
# Send OTP to the specified email address
def send_otp(email, otp):
    sender_email = "oipmakeyourown@gmail.com"  # Your email address
    sender_password = "vvrd tais gzrz krqf"  # Your email password
    subject = "OTP for verification"
    message = f"Your OTP for verification is: {otp}"
 
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = email
    msg['Subject'] = subject
 
    msg.attach(MIMEText(message, 'plain'))
 
    try:
       
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, email, text)
        server.quit()
        return True
    except Exception as e:
        print("Error sending email:", str(e))
        return False

@app.route('/send_otp', methods=['POST'])
def send_otp_route():
    db = get_db_connection()
    if db is None:
        return jsonify({'error': 'Failed to connect to database'}), 500

    cursor = db.cursor()
    email = request.json.get('email')
    if not email:
        close_db_connection(db)
        return jsonify({'error': 'Email address not provided'}), 400
    
    try:
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        result = cursor.fetchone()
        if result:
            close_db_connection(db)
            return jsonify({'error': 'User already exists'}), 400
    except Exception as e:
        close_db_connection(db)
        return jsonify({'error': str(e)}), 500

    otp = generate_otp()
    if send_otp(email, otp):
        cursor.execute("INSERT INTO otp (otp_value, used, email) VALUES (%s, %s, %s)", (otp, 0, email))
        db.commit()
        close_db_connection(db)
        return jsonify({'message': 'OTP sent successfully'}), 200
    else:
        close_db_connection(db)
        return jsonify({'error': 'Failed to send OTP'}), 500

@app.route('/login', methods=['POST'])
def login():
    db = get_db_connection()
    if db is None:
        return jsonify({'error': 'Failed to connect to database'}), 500

    cursor = db.cursor(dictionary=True)  # Ensure dictionary=True for fetching results as dictionaries
    email = request.json.get('email')
    password = request.json.get('password')

    if not email or not password:
        close_db_connection(db)
        return jsonify({'error': 'Email and password are required'}), 400

    try:
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        if not user or user['password'] != password:
            close_db_connection(db)
            return jsonify({'error': 'Invalid username or password'}), 401

        close_db_connection(db)
        return jsonify({'message': 'Login successful'}), 200
    except mysql.connector.Error as err:
        close_db_connection(db)
        return jsonify({'error': f'Database error: {str(err)}'}), 500


@app.route('/add_user', methods=['POST'])
def add_user():
    db = get_db_connection()
    if db is None:
        return jsonify({'error': 'Failed to connect to database'}), 500

    cursor = db.cursor()
    email = request.json.get('email')
    password = request.json.get('password')

    if not email or not password:
        close_db_connection(db)
        return jsonify({'error': 'All fields are required'}), 400

    try:
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        if cursor.fetchone():
            close_db_connection(db)
            return jsonify({'error': 'User already exists'}), 400

        cursor.execute("INSERT INTO users (email, password) VALUES (%s, %s)", (email, password))
        db.commit()
        close_db_connection(db)
        return jsonify({'message': 'User added successfully'}), 200
    except mysql.connector.Error as err:
        close_db_connection(db)
        return jsonify({'error': f'Database error: {str(err)}'}), 500


@app.route('/update_password', methods=['POST'])
def update_password():
    db = get_db_connection()
    if db is None:
        return jsonify({'error': 'Failed to connect to database'}), 500

    cursor = db.cursor()
    email = request.json.get('email')
    new_password = request.json.get('new_password')

    if not email or not new_password:
        close_db_connection(db)
        return jsonify({'error': 'Email and new password are required'}), 400

    try:
        cursor.execute("UPDATE users SET password = %s WHERE email = %s", (new_password, email))
        db.commit()
        close_db_connection(db)
        return jsonify({'message': 'Password updated successfully'}), 200
    except mysql.connector.Error as err:
        close_db_connection(db)
        return jsonify({'error': f'Database error: {str(err)}'}), 500


@app.route('/validate_otp', methods=['POST'])
def validate_otp():
    db = get_db_connection()
    if db is None:
        return jsonify({'error': 'Failed to connect to database'}), 500

    cursor = db.cursor()
    otp = request.json.get('otp')
    email = request.json.get('email')

    if not otp or not email:
        close_db_connection(db)
        return jsonify({'error': 'OTP or email not provided'}), 400

    try:
        query = "SELECT * FROM otp WHERE otp_value = %s AND used = FALSE AND email = %s"
        cursor.execute(query, (otp, email))
        otp_entry = cursor.fetchone()

        if otp_entry:
            update_query = "UPDATE otp SET used = TRUE WHERE id = %s"
            cursor.execute(update_query, (otp_entry[0],))
            db.commit()
            close_db_connection(db)
            return jsonify({'message': 'OTP is valid'}), 200
        else:
            close_db_connection(db)
            return jsonify({'error': 'Invalid OTP or OTP already used'}), 400
    except mysql.connector.Error as e:
        close_db_connection(db)
        return jsonify({'error': f'Error accessing database: {str(e)}'}), 500


@app.route('/check_email', methods=['POST'])
def check_email():
    db = get_db_connection()
    if db is None:
        return jsonify({'error': 'Failed to connect to database'}), 500

    cursor = db.cursor()
    data = request.get_json()
    email = data.get('email')

    if not email:
        close_db_connection(db)
        return jsonify({'error': 'Email parameter is missing'}), 400

    try:
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        result = cursor.fetchone()
        if result:
            close_db_connection(db)
            return jsonify({'exists': True}), 200
        else:
            close_db_connection(db)
            return jsonify({'exists': False}), 404
    except mysql.connector.Error as e:
        close_db_connection(db)
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    # Configure Flask port using an environment variable
    app.run(host='0.0.0.0', port=5505)
