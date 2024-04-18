from flask import Flask, request, jsonify, session ,json
# pythonanywhere
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a secure secret key in productio
# Dummy storage for valid tokens (in a real-world scenario, use a secure method like a database)
valid_tokens = set()
grant_type_access = 'client_credentials'
grant_type_UMA = 'urn:ietf:params:oauth:grant-type:uma-ticket'
client_id = 'healthcare'
@app.route('/')
def hello_IOT():
    #defib_data = session.get('defib_data', 'No data available')
    defibdata = session.get('defib_data')
    return f'Site_version: v1.1 - python anywhere - Defib_data: {defibdata}'
@app.route('/auth/realms/healthcare/protocol/openid-connect/token', methods=['POST'])
def login():
    #data = request.get_json()
    data = request.form.to_dict()
    print("Received Data:",data)

    # Check if user id and password are provided in the request
    if 'grant_type' in data:
        received_grant_type=data['grant_type']
        if received_grant_type == grant_type_access:
            print("Access Token is Requested")
            if 'DeviceName' in data:
                Device_Name = data['DeviceName']
                print("Device Name:",Device_Name)
                #Defib_data = data['Defib']
                #Defib_data = data['Defib']
                #print("Defib received as:",Defib_data)
                # Store 'Defib_data' in the session
                #session['defib_data'] =Device_Name
                session['defib_data'] = data.get('DeviceName', 'No Defib data provided')
                # Perform authentication logic using user_id and password
                # Generate authentication and authorization tokens
            else:
                Device_Name='No Device Name Found'
            Token_type='Access'
            auth_token = generate_auth_token(Token_type)
            #auth_header = {'Authorization': f'Bearer {auth_token}'}
            auth_header = {'Authorization': auth_token}
            # Store the valid token (in a real-world scenario, use a secure method like a database)
            #valid_tokens.add(auth_token)
            return jsonify(auth_token) ,200
        if received_grant_type == grant_type_UMA:
            print("UMA Token is Requested")
            Token_type='UMA'
            auth_token = generate_auth_token(Token_type)
            return jsonify(auth_token) ,200
        else:
            print("Unexpected client ID id is received:",Device_Name)
            # For demonstration purposes, let's just return a success message with the tokens
            #return jsonify({'message': f'Login successful for user {client_id}', 'tokens': auth_header}), 200
            return jsonify({'error': 'Unexpected client ID id is received:'}), 400
    else:
        return jsonify({'error': 'User id are required'}), 400
    

def generate_auth_token(Token_type):
    # In a real-world scenario, you should implement a proper token generation mechanism
    # This can be done using libraries like PyJWT for JSON Web Tokens
    # For demonstration purposes, let's just concatenate user_id with a secret key
    if Token_type == 'Access':
        with open('access_token.json', 'r') as file:
            accessToken = json.load(file)
        # Additional parameters for x-www-form-urlencoded
        print("Read json is Access: ",accessToken)
        # Create a dictionary to represent the form data
        #data = {
        #    'access_token':accessToken
        #}
        # Use requests to send a POST request with x-www-form-urlencoded data
        #response = requests.post('your_token_endpoint_url', data=data)
        #return f'{user_id}_{data}'
        #return f'{data}'
        return accessToken
    if Token_type == 'UMA':
        with open('UMA_token.json', 'r') as file:
            UMAToken = json.load(file)
        # Additional parameters for x-www-form-urlencoded
        print("Read json is UMA: ",UMAToken)
        # Create a dictionary to represent the form data
        #data = {
        #    'access_token':accessToken
        #}
        # Use requests to send a POST request with x-www-form-urlencoded data
        #response = requests.post('your_token_endpoint_url', data=data)
        #return f'{user_id}_{data}'
        #return f'{data}'
        return UMAToken

@app.route('/validate', methods=['POST'])
def validate_token():
    token = request.headers.get('Authorization', '').replace('Bearer ', '')

    # Check if the token is valid
    if token in valid_tokens:
        return jsonify({'message': 'Token is valid'}), 200
    else:
        return jsonify({'error': 'Invalid token'}), 401
@app.route('/ingestion/healthcare/ngsi-ld/v1/entities/urn:ngsi-ld:Defibrillator:1',methods=['POST'])
def DefibrillatorInfo_Page():
    #data = request.form.to_dict()
    data = request.get_json()
    print("Cihaz Bilgi mesaji:\n",data)
    return jsonify({'message': 'Cihaz Bilgi Mesaji Alindi'}),201
@app.route('/ingestion/healthcare/ngsi-ld/v1/entities/urn:ngsi-DefibrillatorTest:1',methods=['POST'])
def DefibrillatorTest_Page():
    data = request.get_json()
    print("Cihaz test mesaji:\n",data)
    return jsonify({'message': 'Cihaz Bilgi Mesaji Alindi'}),201
@app.route('/ingestion/healthcare/ngsi-ld/v1/entities/urn:ngsi-DefibrillatorPosition:2',methods=['POST'])
def DefibrillatorLocation_Page():
    data = request.get_json()
    print("Lokasyon mesaji:\n",data)
    return jsonify({'message': 'Lokasyon Mesaji Alindi'}),201
@app.route('/ingestion/healthcare/ngsi-ld/v1/entities/urn:ngsi-HealthCase:1',methods=['POST'])
def CreateHealtCase_Page():
    data = request.get_json()
    print("Create Health Case mesaji:\n",data)
    return jsonify({'message': 'Create Health Case mesaji Alindi'}),201
if __name__ == '__main__':
    app.run(debug=True)


