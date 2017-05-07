from flask import Flask, request
import json
import requests

app = Flask(__name__)

PAGE_ACCESS_TOKEN = 'EAAP91RO7gI0BANShZAIznz5Eksjj4QG2gLyJ2sCV7bk3btkevxIBocHRdZABWz0C0TYPjZCWsfz06A4xIUdnJ0T2A8cQRbKXx0gAsX0Wn1qOzb5ZChaIELE9ZC7G2eMDlFTZC4VWz3XoXzfG5dkAZBlRVG5ZAISIgWJ8BKZBP4Wuk5QZDZD'

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
    entry = messageObj['entry'][0]
    responseMessage = ''

    if 'messaging' in entry:
        message = entry['messaging'][0]['message']
        senderId = entry['messaging'][0]['sender']['id']
        if 'attachments' in message:

            attachments = message['attachments'][0]

            if attachments['type'] == 'location':

                coordinates = attachments['payload']['coordinates']

                responseMessage += 'Your location is '+str(coordinates['lat'])+','+str(coordinates['long'])

        if 'text' in message:
            responseMessage = 'You said,"'+message['text']+'"'
        
        sendResponse(senderId,responseMessage)
    else:
        responseMessage = 'I don\'t understand what you said'
        

    return responseMessage

def sendResponse(recipientId,message):

    messageData = {
        'recipient': {
            'id': recipientId
        },
        'message': {
            'text': message
        }
    }

    url = 'https://graph.facebook.com/v2.6/me/messages?access_token='+PAGE_ACCESS_TOKEN

    r = requests.post(url, json = messageData)

    print r.status_code




if __name__ == '__main__':
    app.run(port=3000, debug=True)