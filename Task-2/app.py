
from flask import Flask, request, jsonify
from auth import create_token, jwt_required
import redis
from utils import is_email_valid
r = redis.Redis()

app = Flask(__name__)
 
@app.route('/', methods=["GET", 'POST'])
@jwt_required()
def set_data():
    if request.method=="POST":
        payload = request.get_json()
        if not payload:
            return "Invalid data provided", 400

        if not payload.get('email'):
            return "email address required", 400

        if not is_email_valid(payload.get('email')):
            return "Invalid email address", 400
        
        token = create_token({"email": payload['email']})
        return token, 201
    
    elif request.method=="GET":
        speed = r.get("speed")
        if not speed:
            return "No data found", 203
        speed = speed.decode()
        return jsonify({"speed": speed}), 200


if __name__ == '__main__':
    app.run(port=4000)