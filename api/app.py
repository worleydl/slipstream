from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO
from redis import Redis

app = Flask(__name__)
CORS(app)
redis = Redis(host='redis', port=6379, decode_responses=True)

@app.route('/')
def default():
    return "SLIPSTREAM"

@app.route('/getQueue', methods=['POST'])
def getQueue():
    payload = request.json
    return jsonify({"items": redis.lrange(payload['token'], 0, -1)})

@app.route('/popStream', methods=['POST'])
def popStream():
    payload = request.json

    token = payload['token']

    return jsonify({'video': redis.lpop(token)})

@app.route('/pushStream', methods=['POST'])
def pushStream():
    payload = request.json

    token = payload['token']
    stream = payload['stream']

    redis.lpush(token, stream)

    return jsonify({'status': 200})

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
