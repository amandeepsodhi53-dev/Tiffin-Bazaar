import os
import random
import string
import jwt
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
from flask import Flask, request, jsonify

load_dotenv()

app = Flask(__name__)

# Configuration
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')

# OTP Generation Function
def generate_otp(length=6):
    digits = string.digits
    otp = ''.join(random.choice(digits) for _ in range(length))
    return otp

# JWT Authentication
def create_token(data):
    return jwt.encode(data, JWT_SECRET_KEY, algorithm='HS256')

def decode_token(token):
    try:
        return jwt.decode(token, JWT_SECRET_KEY, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

# Email Validation Function
def is_valid_email(email):
    import re
    return re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email) is not None

# Error Handling Middleware
@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': 'Bad request', 'message': str(error)}), 400

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error', 'message': 'An unexpected error occurred'}), 500

# Example endpoint to send OTP
@app.route('/send_otp', methods=['POST'])
def send_otp():
    email = request.json.get('email')
    if not is_valid_email(email):
        return jsonify({'error': 'Invalid email format'}), 400
    otp = generate_otp()
    # Here, the code to send the email would be implemented using smtplib or similar

    return jsonify({'otp': otp}), 200

if __name__ == '__main__':
    app.run(debug=True)