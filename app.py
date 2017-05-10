from flask import Flask, request
import json
import requests

app = Flask(__name__)

PAGE_ACCESS_TOKEN = 'b9e59541f0bb435e86c52a4a0c373d4a'
API_AI_CLIENT_ACCESS_TOKEN = 'EAAaSNJZBwftIBAC1lYVgmOrlIVVjQnXmw4mXG77bg4tWvtZAeAxfx1owmj7rbiZAgG5GZBYotz7wUFE9mXCbGZBg0bPt1mvDmjcZBFnFKukLmZBaON2ajdot3iewuZCdBQYB6ibCo6MZASAiezhsUt6xZB9DTW2wtsKu7vwrivcnjnegZDZD'


user = {

}

@app.route('/locationfinder',methods=['GET'])
def verify():

    if request.args['hub.verify_token'] == 'rukmani':
        print request.args['hub.challenge']
        return request.args['hub.challenge']
    else:
        return "Error", 403

@app.route('/locationfinder',methods=['POST'])
def message():
    print "Request received from facebook"
    messageObj = json.loads(request.data)
    entry = messageObj['entry'][0]
    responseMessage = ''

    if 'messaging' in entry:
        message = entry['messaging'][0]['message']
        senderId = entry['messaging'][0]['sender']['id']
        
        #if it is a text message
        if 'text' in message:
            reply(senderId,message['text'],False)

            #apiResponse = sendToApiAi(message['text'],senderId)
            #handleApiResponse(apiResponse,senderId)
            


        #If we get the location from user
        if 'attachments' in message:
            attachments = message['attachments'][0]
            if attachments['type'] == 'location':
                reply(senderId,attachments['payload']['coordinates'],True)

                #coordinates = attachments['payload']['coordinates']
                #responseMessage += 'Your location is '+str(coordinates['lat'])+','+str(coordinates['long'])
                #sendResponse(responseMessage,senderId)
        
                

    return "Success", 200




def reply(senderId,messageData,isLocationMessage=False):

    if senderId not in user:
        user[str(senderId)] = {
            'cuisine':None,
            'location':None
        }

    if isLocationMessage:

        user[senderId]['location'] = {
            'lat': str(messageData['lat']),
            'long': str(messageData['long'])
        }

        if user[senderId]['cuisine']:

            #### Call rest api of that guy
            sendRestaurantsList(senderId,user[senderId]['cuisine'])
            return
        
        else:
            responseMessage = "What are you looking to eat ?"
            sendResponse(senderId,responseMessage)
    else:
        apiResponse = sendToApiAi(messageData,senderId)
        handleApiResponse(apiResponse,senderId)


def sendToApiAi(text,senderId):

    messageData = {
        'query':text,
        'lang':'en',
        'sessionId':senderId
    }

    headers = {'Authorization': 'bearer '+API_AI_CLIENT_ACCESS_TOKEN}

    url = 'https://api.api.ai/v1/query?v=20150910'

    r = requests.post(url, json=messageData, headers = headers)

    return r.json()


def handleApiResponse(apiResponse,senderId):

    responseMessage = "I don't understand what you said"
    print apiResponse
    if 'result' in apiResponse:
        result = apiResponse['result']
        
        if 'action' in result:
            action = result['action']

            if action == 'looking':
                
                if 'cuisine' in result['parameters']:
                    user[senderId]['cuisine'] = result['parameters']['cuisine']

                    if user[senderId]['location']:
                        sendRestaurantsList(senderId,user[senderId]['cuisine'])
                        return
                    else:
                        sendAskForLocation(senderId)
                        return
    
    sendResponse(senderId,responseMessage)
        


def sendAskForLocation(recipientId):

    messageData = {
        'recipient': {
            'id': recipientId
        },
        'message': {
            'text': 'Please share your location',
            "quick_replies":[
                {
                    "content_type":"location",
                }
            ]
        }
    }

    url = 'https://graph.facebook.com/v2.6/me/messages?access_token='+PAGE_ACCESS_TOKEN

    r = requests.post(url, json = messageData)

    print r.status_code


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


def sendRestaurantsList(receipientId,cuisine):

    responseMessage = "Finding all "+cuisine+" resturants near you"
    sendResponse(receipientId,responseMessage)
    del user[receipientId]


if __name__ == '__main__':
    app.run(port=3000, debug=True)