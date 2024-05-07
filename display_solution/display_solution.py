from flask import Flask, jsonify
import mysql.connector
from flask_cors import CORS
import os


app = Flask(__name__)
CORS(app)
db_config = {
    'host': os.getenv('DB_HOST'),
    'port':int(os.getenv('DB_PORT')),
    'user': os.getenv('DB_USER','root'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME','test_db')
}


@app.route('/get_use_cases1', methods=['GET'])
def get_use_cases1():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT UC_ID, Use_Case FROM bausecase")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        use_cases = [{'UCID': row[0], 'use_case_name': row[1]} for row in rows]
        return jsonify(use_cases)
    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 500

# if __name__ == '__main__':
#     app.run(host='0.0.0.0',port=5005)

if __name__ == '__main__':
    # Use environment variable for the port or default to 5006 if not set
    app.run(host='0.0.0.0', port=5005)



