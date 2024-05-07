from flask import Flask, jsonify, request
from flask_restx import Api, Resource
from flask_cors import CORS
import mysql.connector
import os

app = Flask(__name__)
CORS(app)
api = Api(app, version='1.0', title='Insurance APIs', description='API for managing insurance data')

# Database Configuration
db_config = {
    'host': os.getenv('DB_HOST'),
    'port':int(os.getenv('DB_PORT')),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME','techinsurance')
}


# Function to connect to MySQL database
def connect_to_db():
    try:
        connection = mysql.connector.connect(**db_config)
        return connection
    except Exception as e:
        print("Error connecting to database:", e)



ns_insurer = api.namespace('insurer',description='<h1 style="font-weight:bold; font-size:4px;"></h1>')
@ns_insurer.route('/vehicle')
class VehicleResource(Resource):
    @api.doc(responses={200: 'OK'}, description='Get all vehicle data')
    def get(self):
        try:
            connection = connect_to_db()
            if connection:
                cursor = connection.cursor(dictionary=True)
                cursor.execute("SELECT * FROM vehicle")
                rows = cursor.fetchall()
                cursor.close()
                connection.close()
                return jsonify({'success': True, 'data': rows})
            else:
                return jsonify({'success': False, 'message': 'Failed to connect to the database'})
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)})
        
@ns_insurer.route('/insert/vehicle')
class AddressResourceInsert(Resource):
    @api.doc(responses={201: 'Created', 400: 'Bad Request'}, description='Insert a new record into the vehicle table')
    def post(self):
        try:
            data = request.get_json()
            if not isinstance(data, dict):
                return {'success': False, 'message': 'Invalid JSON format'}, 400

            # Connect to the database
            connection = connect_to_db()
            if not connection:
                return {'success': False, 'message': 'Failed to connect to database'}, 500

            cursor = connection.cursor()
            column_names = list(data.keys())
            column_values = list(data.values())
            placeholders = ', '.join(['%s' for _ in range(len(column_names))])
            query = f"INSERT INTO vehicle ({', '.join(column_names)}) VALUES ({placeholders})"
            cursor.execute(query, column_values)
            connection.commit()
            cursor.close()
            connection.close()

            return {'success': True, 'message': 'Record inserted successfully'}, 201
        except Exception as e:
            return {'success': False, 'message': str(e)}, 400



# Define similar routes for other table names...
@ns_insurer.route('/claim')
class ClaimResource(Resource):
    @api.doc(responses={200: 'OK'}, description='Get all claim data')
    def get(self):
        try:
            connection = connect_to_db()
            if connection:
                cursor = connection.cursor(dictionary=True)
                cursor.execute("SELECT * FROM claim")
                rows = cursor.fetchall()
                cursor.close()
                connection.close()
                return jsonify({'success': True, 'data': rows})
            else:
                return jsonify({'success': False, 'message': 'Failed to connect to the database'})
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)})
        
@ns_insurer.route('/insert/claim')
class AddressResourceInsert(Resource):
    @api.doc(responses={201: 'Created', 400: 'Bad Request'}, description='Insert a new record into the claim table')
    def post(self):
        try:
            data = request.get_json()
            if not isinstance(data, dict):
                return {'success': False, 'message': 'Invalid JSON format'}, 400

            # Connect to the database
            connection = connect_to_db()
            if not connection:
                return {'success': False, 'message': 'Failed to connect to database'}, 500

            cursor = connection.cursor()
            column_names = list(data.keys())
            column_values = list(data.values())
            placeholders = ', '.join(['%s' for _ in range(len(column_names))])
            query = f"INSERT INTO claim ({', '.join(column_names)}) VALUES ({placeholders})"
            cursor.execute(query, column_values)
            connection.commit()
            cursor.close()
            connection.close()

            return {'success': True, 'message': 'Record inserted successfully'}, 201
        except Exception as e:
            return {'success': False, 'message': str(e)}, 400

        
@ns_insurer.route('/driver')
class DriverResource(Resource):
    @api.doc(responses={200: 'OK'}, description='Get all driver data')
    def get(self):
        try:
            connection = connect_to_db()
            if connection:
                cursor = connection.cursor(dictionary=True)
                cursor.execute("SELECT * FROM driver")
                rows = cursor.fetchall()
                cursor.close()
                connection.close()
                return jsonify({'success': True, 'data': rows})
            else:
                return jsonify({'success': False, 'message': 'Failed to connect to the database'})
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)})
        

@ns_insurer.route('/insert/driver')
class AddressResourceInsert(Resource):
    @api.doc(responses={201: 'Created', 400: 'Bad Request'}, description='Insert a new record into the driver table')
    def post(self):
        try:
            data = request.get_json()
            if not isinstance(data, dict):
                return {'success': False, 'message': 'Invalid JSON format'}, 400

            # Connect to the database
            connection = connect_to_db()
            if not connection:
                return {'success': False, 'message': 'Failed to connect to database'}, 500

            cursor = connection.cursor()
            column_names = list(data.keys())
            column_values = list(data.values())
            placeholders = ', '.join(['%s' for _ in range(len(column_names))])
            query = f"INSERT INTO driver ({', '.join(column_names)}) VALUES ({placeholders})"
            cursor.execute(query, column_values)
            connection.commit()
            cursor.close()
            connection.close()

            return {'success': True, 'message': 'Record inserted successfully'}, 201
        except Exception as e:
            return {'success': False, 'message': str(e)}, 400



# Define similar routes for other table names
@ns_insurer.route('/beneficiary')
class BeneficiaryResource(Resource):
    @api.doc(responses={200: 'OK'}, description='Get all beneficiaries')
    def get(self):
        try:
            connection = connect_to_db()
            if connection:
                cursor = connection.cursor(dictionary=True)
                cursor.execute("SELECT * FROM beneficiary")
                rows = cursor.fetchall()
                cursor.close()
                connection.close()
                return jsonify({'success': True, 'data': rows})
            else:
                return jsonify({'success': False, 'message': 'Failed to connect to the database'})
        except Exception as e:
        # Logic to get beneficiaries from the database
            return jsonify({'success': True, 'data': 'Beneficiary data'})
        
@ns_insurer.route('/insert/beneficiary')
class AddressResourceInsert(Resource):
    @api.doc(responses={201: 'Created', 400: 'Bad Request'}, description='Insert a new record into the beneficiary table')
    def post(self):
        try:
            data = request.get_json()
            if not isinstance(data, dict):
                return {'success': False, 'message': 'Invalid JSON format'}, 400

            # Connect to the database
            connection = connect_to_db()
            if not connection:
                return {'success': False, 'message': 'Failed to connect to database'}, 500

            cursor = connection.cursor()
            column_names = list(data.keys())
            column_values = list(data.values())
            placeholders = ', '.join(['%s' for _ in range(len(column_names))])
            query = f"INSERT INTO beneficiary ({', '.join(column_names)}) VALUES ({placeholders})"
            cursor.execute(query, column_values)
            connection.commit()
            cursor.close()
            connection.close()

            return {'success': True, 'message': 'Record inserted successfully'}, 201
        except Exception as e:
            return {'success': False, 'message': str(e)}, 400




# Define resources for each endpoint
@ns_insurer.route('/address')
class AddressResource(Resource):
    @api.doc(description='### Addresses\nGet all addresses')
    def get(self):
        try:
            connection = connect_to_db()
            if connection:
                cursor = connection.cursor(dictionary=True)
                cursor.execute("SELECT * FROM address")
                rows = cursor.fetchall()
                cursor.close()
                connection.close()
                return jsonify({'success': True, 'data': rows})
            else:
                return jsonify({'success': False, 'message': 'Failed to connect to the database'})
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)})
        
@ns_insurer.route('/insert/address')
class AddressResourceInsert(Resource):
    @api.doc(responses={201: 'Created', 400: 'Bad Request'}, description='Insert a new record into the address table')
    def post(self):
        try:
            data = request.get_json()
            if not isinstance(data, dict):
                return {'success': False, 'message': 'Invalid JSON format'}, 400

            # Connect to the database
            connection = connect_to_db()
            if not connection:
                return {'success': False, 'message': 'Failed to connect to database'}, 500

            cursor = connection.cursor()
            column_names = list(data.keys())
            column_values = list(data.values())
            placeholders = ', '.join(['%s' for _ in range(len(column_names))])
            query = f"INSERT INTO address ({', '.join(column_names)}) VALUES ({placeholders})"
            cursor.execute(query, column_values)
            connection.commit()
            cursor.close()
            connection.close()

            return {'success': True, 'message': 'Record inserted successfully'}, 201
        except Exception as e:
            return {'success': False, 'message': str(e)}, 400




# Define similar routes for other tables...
@ns_insurer.route('/conviction')
class ConvictionResource(Resource):
    @api.doc(responses={200: 'OK'}, description='Get all conviction data')
    def get(self):
        try:
            connection = connect_to_db()
            if connection:
                cursor = connection.cursor(dictionary=True)
                cursor.execute("SELECT * FROM conviction")
                rows = cursor.fetchall()
                cursor.close()
                connection.close()
                return jsonify({'success': True, 'data': rows})
            else:
                return jsonify({'success': False, 'message': 'Failed to connect to the database'})
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)})
        
@ns_insurer.route('/insert/conviction')
class AddressResourceInsert(Resource):
    @api.doc(responses={201: 'Created', 400: 'Bad Request'}, description='Insert a new record into the conviction table')
    def post(self):
        try:
            data = request.get_json()
            if not isinstance(data, dict):
                return {'success': False, 'message': 'Invalid JSON format'}, 400

            # Connect to the database
            connection = connect_to_db()
            if not connection:
                return {'success': False, 'message': 'Failed to connect to database'}, 500

            cursor = connection.cursor()
            column_names = list(data.keys())
            column_values = list(data.values())
            placeholders = ', '.join(['%s' for _ in range(len(column_names))])
            query = f"INSERT INTO conviction ({', '.join(column_names)}) VALUES ({placeholders})"
            cursor.execute(query, column_values)
            connection.commit()
            cursor.close()
            connection.close()

            return {'success': True, 'message': 'Record inserted successfully'}, 201
        except Exception as e:
            return {'success': False, 'message': str(e)}, 400

        
# Define similar routes for other tables...
@ns_insurer.route('/drivinglicence')
class DrivingLicenceResource(Resource):
    @api.doc(responses={200: 'OK'}, description='Get all driving licence data')
    def get(self):
        try:
            connection = connect_to_db()
            if connection:
                cursor = connection.cursor(dictionary=True)
                cursor.execute("SELECT * FROM drivinglicence")
                rows = cursor.fetchall()
                cursor.close()
                connection.close()
                return jsonify({'success': True, 'data': rows})
            else:
                return jsonify({'success': False, 'message': 'Failed to connect to the database'})
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)})
        
@ns_insurer.route('/insert/drivinglicence')
class AddressResourceInsert(Resource):
    @api.doc(responses={201: 'Created', 400: 'Bad Request'}, description='Insert a new record into the drivinglicence table')
    def post(self):
        try:
            data = request.get_json()
            if not isinstance(data, dict):
                return {'success': False, 'message': 'Invalid JSON format'}, 400

            # Connect to the database
            connection = connect_to_db()
            if not connection:
                return {'success': False, 'message': 'Failed to connect to database'}, 500

            cursor = connection.cursor()
            column_names = list(data.keys())
            column_values = list(data.values())
            placeholders = ', '.join(['%s' for _ in range(len(column_names))])
            query = f"INSERT INTO drivinglicence ({', '.join(column_names)}) VALUES ({placeholders})"
            cursor.execute(query, column_values)
            connection.commit()
            cursor.close()
            connection.close()

            return {'success': True, 'message': 'Record inserted successfully'}, 201
        except Exception as e:
            return {'success': False, 'message': str(e)}, 400


ns_insurance = api.namespace('insurance',description='<h1 style="font-weight:bold; font-size:4px;"></h1>')

@ns_insurance.route('/motorcoverage')
class MotorCoverageResource(Resource):
    @api.doc(responses={200: 'OK'}, description='Get all motor coverage data')
    def get(self):
        try:
            connection = connect_to_db()
            if connection:
                cursor = connection.cursor(dictionary=True)
                cursor.execute("SELECT * FROM motorcoverage")
                rows = cursor.fetchall()
                cursor.close()
                connection.close()
                return jsonify({'success': True, 'data': rows})
            else:
                return jsonify({'success': False, 'message': 'Failed to connect to the database'})
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)})
        

@ns_insurance.route('/insert/motorcoverage')
class AddressResourceInsert(Resource):
    @api.doc(responses={201: 'Created', 400: 'Bad Request'}, description='Insert a new record into the motorcoverage table')
    def post(self):
        try:
            data = request.get_json()
            if not isinstance(data, dict):
                return {'success': False, 'message': 'Invalid JSON format'}, 400

            # Connect to the database
            connection = connect_to_db()
            if not connection:
                return {'success': False, 'message': 'Failed to connect to database'}, 500

            cursor = connection.cursor()
            column_names = list(data.keys())
            column_values = list(data.values())
            placeholders = ', '.join(['%s' for _ in range(len(column_names))])
            query = f"INSERT INTO motorcoverage ({', '.join(column_names)}) VALUES ({placeholders})"
            cursor.execute(query, column_values)
            connection.commit()
            cursor.close()
            connection.close()

            return {'success': True, 'message': 'Record inserted successfully'}, 201
        except Exception as e:
            return {'success': False, 'message': str(e)}, 400


        
   
@ns_insurance.route('/insuranceentity')
class InsuranceEntityResource(Resource):
    @api.doc(responses={200: 'OK'}, description='Get all insurance entity data')
    def get(self):
        try:
            connection = connect_to_db()
            if connection:
                cursor = connection.cursor(dictionary=True)
                cursor.execute("SELECT * FROM insuranceentity")
                rows = cursor.fetchall()
                cursor.close()
                connection.close()
                return jsonify({'success': True, 'data': rows})
            else:
                return jsonify({'success': False, 'message': 'Failed to connect to the database'})
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)})
        
@ns_insurance.route('/insert/insuranceentity')
class AddressResourceInsert(Resource):
    @api.doc(responses={201: 'Created', 400: 'Bad Request'}, description='Insert a new record into the insuranceentity table')
    def post(self):
        try:
            data = request.get_json()
            if not isinstance(data, dict):
                return {'success': False, 'message': 'Invalid JSON format'}, 400

            # Connect to the database
            connection = connect_to_db()
            if not connection:
                return {'success': False, 'message': 'Failed to connect to database'}, 500

            cursor = connection.cursor()
            column_names = list(data.keys())
            column_values = list(data.values())
            placeholders = ', '.join(['%s' for _ in range(len(column_names))])
            query = f"INSERT INTO insuranceentity ({', '.join(column_names)}) VALUES ({placeholders})"
            cursor.execute(query, column_values)
            connection.commit()
            cursor.close()
            connection.close()

            return {'success': True, 'message': 'Record inserted successfully'}, 201
        except Exception as e:
            return {'success': False, 'message': str(e)}, 400
        

@ns_insurance.route('/personal')
class PersonalResource(Resource):
    @api.doc(responses={200: 'OK'}, description='Get all personal data')
    def get(self):
        try:
            connection = connect_to_db()
            if connection:
                cursor = connection.cursor(dictionary=True)
                cursor.execute("SELECT * FROM personal")
                rows = cursor.fetchall()
                cursor.close()
                connection.close()
                return jsonify({'success': True, 'data': rows})
            else:
                return jsonify({'success': False, 'message': 'Failed to connect to the database'})
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)})
        
@ns_insurance.route('/insert/personal')
class AddressResourceInsert(Resource):
    @api.doc(responses={201: 'Created', 400: 'Bad Request'}, description='Insert a new record into the personal table')
    def post(self):
        try:
            data = request.get_json()
            if not isinstance(data, dict):
                return {'success': False, 'message': 'Invalid JSON format'}, 400

            # Connect to the database
            connection = connect_to_db()
            if not connection:
                return {'success': False, 'message': 'Failed to connect to database'}, 500

            cursor = connection.cursor()
            column_names = list(data.keys())
            column_values = list(data.values())
            placeholders = ', '.join(['%s' for _ in range(len(column_names))])
            query = f"INSERT INTO personal ({', '.join(column_names)}) VALUES ({placeholders})"
            cursor.execute(query, column_values)
            connection.commit()
            cursor.close()
            connection.close()

            return {'success': True, 'message': 'Record inserted successfully'}, 201
        except Exception as e:
            return {'success': False, 'message': str(e)}, 400
        



@ns_insurance.route('/commercial')
class CommercialResource(Resource):
    @api.doc(responses={200: 'OK'}, description='Get all commercial data')
    def get(self):
        try:
            connection = connect_to_db()
            if connection:
                cursor = connection.cursor(dictionary=True)
                cursor.execute("SELECT * FROM commercial")
                rows = cursor.fetchall()
                cursor.close()
                connection.close()
                return jsonify({'success': True, 'data': rows})
            else:
                return jsonify({'success': False, 'message': 'Failed to connect to the database'})
        except Exception as e:
        # Logic to get commercial data from the database
            return jsonify({'success': True, 'data': 'Commercial data'})


@ns_insurance.route('/insert/commercial')
class AddressResourceInsert(Resource):
    @api.doc(responses={201: 'Created', 400: 'Bad Request'}, description='Insert a new record into the commercial table')
    def post(self):
        try:
            data = request.get_json()
            if not isinstance(data, dict):
                return {'success': False, 'message': 'Invalid JSON format'}, 400

            # Connect to the database
            connection = connect_to_db()
            if not connection:
                return {'success': False, 'message': 'Failed to connect to database'}, 500

            cursor = connection.cursor()
            column_names = list(data.keys())
            column_values = list(data.values())
            placeholders = ', '.join(['%s' for _ in range(len(column_names))])
            query = f"INSERT INTO commercial ({', '.join(column_names)}) VALUES ({placeholders})"
            cursor.execute(query, column_values)
            connection.commit()
            cursor.close()
            connection.close()

            return {'success': True, 'message': 'Record inserted successfully'}, 201
        except Exception as e:
            return {'success': False, 'message': str(e)}, 400
        

@ns_insurance.route('/product')
class ProductResource(Resource):
    @api.doc(responses={200: 'OK'}, description='Get all product data')
    def get(self):
        try:
            connection = connect_to_db()
            if connection:
                cursor = connection.cursor(dictionary=True)
                cursor.execute("SELECT * FROM product")
                rows = cursor.fetchall()
                cursor.close()
                connection.close()
                return jsonify({'success': True, 'data': rows})
            else:
                return jsonify({'success': False, 'message': 'Failed to connect to the database'})
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)})
        


@ns_insurance.route('/insert/product')
class AddressResourceInsert(Resource):
    @api.doc(responses={201: 'Created', 400: 'Bad Request'}, description='Insert a new record into the product table')
    def post(self):
        try:
            data = request.get_json()
            if not isinstance(data, dict):
                return {'success': False, 'message': 'Invalid JSON format'}, 400

            # Connect to the database
            connection = connect_to_db()
            if not connection:
                return {'success': False, 'message': 'Failed to connect to database'}, 500

            cursor = connection.cursor()
            column_names = list(data.keys())
            column_values = list(data.values())
            placeholders = ', '.join(['%s' for _ in range(len(column_names))])
            query = f"INSERT INTO product ({', '.join(column_names)}) VALUES ({placeholders})"
            cursor.execute(query, column_values)
            connection.commit()
            cursor.close()
            connection.close()

            return {'success': True, 'message': 'Record inserted successfully'}, 201
        except Exception as e:
            return {'success': False, 'message': str(e)}, 400


@ns_insurance.route('/premiumbordereau')
class PremiumBordereauResource(Resource):
    @api.doc(responses={200: 'OK'}, description='Get all premium bordereau data')
    def get(self):
        try:
            connection = connect_to_db()
            if connection:
                cursor = connection.cursor(dictionary=True)
                cursor.execute("SELECT * FROM premiumbordereau")
                rows = cursor.fetchall()
                cursor.close()
                connection.close()
                return jsonify({'success': True, 'data': rows})
            else:
                return jsonify({'success': False, 'message': 'Failed to connect to the database'})
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)})


@ns_insurance.route('/insert/premiumbordereau')
class AddressResourceInsert(Resource):
    @api.doc(responses={201: 'Created', 400: 'Bad Request'}, description='Insert a new record into the premiumbordereau table')
    def post(self):
        try:
            data = request.get_json()
            if not isinstance(data, dict):
                return {'success': False, 'message': 'Invalid JSON format'}, 400

            # Connect to the database
            connection = connect_to_db()
            if not connection:
                return {'success': False, 'message': 'Failed to connect to database'}, 500

            cursor = connection.cursor()
            column_names = list(data.keys())
            column_values = list(data.values())
            placeholders = ', '.join(['%s' for _ in range(len(column_names))])
            query = f"INSERT INTO premiumbordereau ({', '.join(column_names)}) VALUES ({placeholders})"
            cursor.execute(query, column_values)
            connection.commit()
            cursor.close()
            connection.close()

            return {'success': True, 'message': 'Record inserted successfully'}, 201
        except Exception as e:
            return {'success': False, 'message': str(e)}, 400
        

@ns_insurance.route('/claimsbordereau')
class ClaimsBordereauResource(Resource):
    @api.doc(responses={200: 'OK'}, description='Get all claims bordereau')
    def get(self):
        try:
            connection = connect_to_db()
            if connection:
                cursor = connection.cursor(dictionary=True)
                cursor.execute("SELECT * FROM claimsbordereau")
                rows = cursor.fetchall()
                cursor.close()
                connection.close()
                return jsonify({'success': True, 'data': rows})
            else:
                return jsonify({'success': False, 'message': 'Failed to connect to the database'})
        except Exception as e:
        # Logic to get claims bordereau from the database
            return jsonify({'success': True, 'data': 'Claims bordereau data'})


@ns_insurance.route('/insert/claimsbordereau')
class AddressResourceInsert(Resource):
    @api.doc(responses={201: 'Created', 400: 'Bad Request'}, description='Insert a new record into the claimsbordereau table')
    def post(self):
        try:
            data = request.get_json()
            if not isinstance(data, dict):
                return {'success': False, 'message': 'Invalid JSON format'}, 400

            # Connect to the database
            connection = connect_to_db()
            if not connection:
                return {'success': False, 'message': 'Failed to connect to database'}, 500

            cursor = connection.cursor()
            column_names = list(data.keys())
            column_values = list(data.values())
            placeholders = ', '.join(['%s' for _ in range(len(column_names))])
            query = f"INSERT INTO claimsbordereau ({', '.join(column_names)}) VALUES ({placeholders})"
            cursor.execute(query, column_values)
            connection.commit()
            cursor.close()
            connection.close()

            return {'success': True, 'message': 'Record inserted successfully'}, 201
        except Exception as e:
            return {'success': False, 'message': str(e)}, 400
        

# Define similar routes for other tables...
@ns_insurance.route('/conviction')
class ConvictionResource(Resource):
    @api.doc(responses={200: 'OK'}, description='Get all conviction data')
    def get(self):
        try:
            connection = connect_to_db()
            if connection:
                cursor = connection.cursor(dictionary=True)
                cursor.execute("SELECT * FROM conviction")
                rows = cursor.fetchall()
                cursor.close()
                connection.close()
                return jsonify({'success': True, 'data': rows})
            else:
                return jsonify({'success': False, 'message': 'Failed to connect to the database'})
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)})

@ns_insurance.route('/insert/conviction')
class AddressResourceInsert(Resource):
    @api.doc(responses={201: 'Created', 400: 'Bad Request'}, description='Insert a new record into the conviction table')
    def post(self):
        try:
            data = request.get_json()
            if not isinstance(data, dict):
                return {'success': False, 'message': 'Invalid JSON format'}, 400

            # Connect to the database
            connection = connect_to_db()
            if not connection:
                return {'success': False, 'message': 'Failed to connect to database'}, 500

            cursor = connection.cursor()
            column_names = list(data.keys())
            column_values = list(data.values())
            placeholders = ', '.join(['%s' for _ in range(len(column_names))])
            query = f"INSERT INTO conviction ({', '.join(column_names)}) VALUES ({placeholders})"
            cursor.execute(query, column_values)
            connection.commit()
            cursor.close()
            connection.close()

            return {'success': True, 'message': 'Record inserted successfully'}, 201
        except Exception as e:
            return {'success': False, 'message': str(e)}, 400



# Define similar routes for other tables...
@ns_insurance.route('/insuranceentity')
class InsuranceEntityResource(Resource):
    @api.doc(responses={200: 'OK'}, description='Get all insurance entity data')
    def get(self):
        try:
            connection = connect_to_db()
            if connection:
                cursor = connection.cursor(dictionary=True)
                cursor.execute("SELECT * FROM insuranceentity")
                rows = cursor.fetchall()
                cursor.close()
                connection.close()
                return jsonify({'success': True, 'data': rows})
            else:
                return jsonify({'success': False, 'message': 'Failed to connect to the database'})
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)})


@ns_insurance.route('/insert/insuranceentity')
class AddressResourceInsert(Resource):
    @api.doc(responses={201: 'Created', 400: 'Bad Request'}, description='Insert a new record into the insuranceentity table')
    def post(self):
        try:
            data = request.get_json()
            if not isinstance(data, dict):
                return {'success': False, 'message': 'Invalid JSON format'}, 400

            # Connect to the database
            connection = connect_to_db()
            if not connection:
                return {'success': False, 'message': 'Failed to connect to database'}, 500

            cursor = connection.cursor()
            column_names = list(data.keys())
            column_values = list(data.values())
            placeholders = ', '.join(['%s' for _ in range(len(column_names))])
            query = f"INSERT INTO insuranceentity ({', '.join(column_names)}) VALUES ({placeholders})"
            cursor.execute(query, column_values)
            connection.commit()
            cursor.close()
            connection.close()

            return {'success': True, 'message': 'Record inserted successfully'}, 201
        except Exception as e:
            return {'success': False, 'message': str(e)}, 400

# Define similar routes for other tables...
@ns_insurance.route('/medicalcondition')
class MedicalConditionResource(Resource):
    @api.doc(responses={200: 'OK'}, description='Get all medical condition data')
    def get(self):
        try:
            connection = connect_to_db()
            if connection:
                cursor = connection.cursor(dictionary=True)
                cursor.execute("SELECT * FROM medicalcondition")
                rows = cursor.fetchall()
                cursor.close()
                connection.close()
                return jsonify({'success': True, 'data': rows})
            else:
                return jsonify({'success': False, 'message': 'Failed to connect to the database'})
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)})


@ns_insurance.route('/insert/medicalcondition')
class AddressResourceInsert(Resource):
    @api.doc(responses={201: 'Created', 400: 'Bad Request'}, description='Insert a new record into the medicalcondition table')
    def post(self):
        try:
            data = request.get_json()
            if not isinstance(data, dict):
                return {'success': False, 'message': 'Invalid JSON format'}, 400

            # Connect to the database
            connection = connect_to_db()
            if not connection:
                return {'success': False, 'message': 'Failed to connect to database'}, 500

            cursor = connection.cursor()
            column_names = list(data.keys())
            column_values = list(data.values())
            placeholders = ', '.join(['%s' for _ in range(len(column_names))])
            query = f"INSERT INTO medicalcondition ({', '.join(column_names)}) VALUES ({placeholders})"
            cursor.execute(query, column_values)
            connection.commit()
            cursor.close()
            connection.close()

            return {'success': True, 'message': 'Record inserted successfully'}, 201
        except Exception as e:
            return {'success': False, 'message': str(e)}, 400


# if __name__ == '__main__':
#     app.run(host='0.0.0.0',port=5050)

if __name__ == '__main__':
    # Use environment variable for the port or default to 5006 if not set
    app.run(host='0.0.0.0', port=int(os.getenv('FLASK_PORT', 5050)))
