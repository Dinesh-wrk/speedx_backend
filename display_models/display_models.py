from flask import Flask, jsonify
import mysql.connector
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Dynamic configuration for MySQL connection using environment variables
db_config = {
    'host': os.getenv('DB_HOST'),
    'port':int(os.getenv('DB_PORT')),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME','models')
}


@app.route('/get_aiuse_cases', methods=['GET'])
def get_aiuse_cases():
    try:
        # Connect to the MySQL database using the configuration from environment variables
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("SELECT Project_ID, Title, Notebook_Filename FROM aiusecase")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        # Create a list of dictionaries to send as JSON
        use_cases = [{'AI_ID': row[0], 'ai_use_case_name': row[1], 'notebook': row[2]} for row in rows]
        return jsonify(use_cases)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Use environment variable for the port or default to 5006 if not set
    app.run(host='0.0.0.0', port=5006)
