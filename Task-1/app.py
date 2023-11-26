from flask import Flask, request
from utils import identify_data, validate_payload, OverlapException
 
app = Flask(__name__)
 
@app.route('/identify', methods=['POST'])

def identify():
    json_data= request.get_json()
    res = validate_payload(json_data)
    if not res:
        return "Invalid payload", 400
    
    try:
        status, data=identify_data(json_data['email'], str(json_data['phoneNumber']))
        return data, 200
    except OverlapException as e:
        return str(e), 400
    except:
        return "Something went wrong", 400


# main driver function
if __name__ == '__main__':
    app.run()