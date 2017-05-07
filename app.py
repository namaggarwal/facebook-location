from flask import Flask, request
import json

app = Flask(__name__)

@app.route('/locationfinder',methods=['GET'])
def verify():

    if request.args['hub.verify_token'] == 'naman':
        print request.args['hub.challenge']
        return request.args['hub.challenge']
    else:
        return "Error", 403

@app.route('/locationfinder',methods=['POST'])
def message():
    messageObj = json.loads(request.data)
    return "naman"




if __name__ == '__main__':
    app.run(port=3000, debug=True)