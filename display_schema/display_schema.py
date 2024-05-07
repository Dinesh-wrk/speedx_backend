from flask import Flask, jsonify
import mysql.connector
from flask_cors import CORS
from mysql.connector import Error
import os

app = Flask(__name__)
CORS(app)

def get_database_connection(db_name):
    """ Utility function to connect to MySQL with environment variables """
    return mysql.connector.connect(
        host=os.getenv('DB_HOST','0.0.0.0'),
        port=int(os.getenv('DB_PORT', '3306')),
        user=os.getenv('DB_USER','root'),
        password=os.getenv('DB_PASSWORD','ConceptVine$@SX#21'),
        database=db_name
    )

def get_database_tables(db_name):
    connection = None
    cursor = None
    try:
        connection = get_database_connection(db_name)
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("SHOW TABLES;")
            tables = cursor.fetchall()
            return [table[0] for table in tables]
    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()
            print("MySQL connection is closed")
    return []

def get_table_schema(db_name, table_name):
    connection = None
    cursor = None
    try:
        connection = get_database_connection(db_name)
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute(f"DESCRIBE `{table_name}`;")
            schema_details = cursor.fetchall()
            return [{'Field': field[0], 'Type': field[1], 'Null': field[2], 'Key': field[3], 'Default': field[4], 'Extra': field[5]} for field in schema_details]
    except Error as e:
        print(f"Error while connecting to MySQL to retrieve schema: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()
            print("MySQL connection is closed")
    return []

@app.route('/schema/<db_name>', methods=['GET'])
def tables(db_name):
    tables = get_database_tables(db_name)
    return jsonify(tables)

@app.route('/schema/<db_name>/<table_name>', methods=['GET'])
def table_schema(db_name, table_name):
    schema = get_table_schema(db_name, table_name)
    return jsonify(schema)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
