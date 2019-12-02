from coapthon.client.helperclient import HelperClient
import json

def message_to_json(message):
    message = json.dumps(message)
    return message
host = "148.213.190.38"
port = 5683


def getUser(pinCode):
    path ="/device/button"
    code = {
        "code": pinCode
    }
    payload = message_to_json(code)
    
    response = None
    result_good = None
    try:
        client = HelperClient(server=(host, port))
        response = client.post(path,payload,None, None)
    except:
        print "Something went wrong, try it againg!"
    else:
        if response:
            print response
            result_good = response.payload() 
            print result_good   
                
    # responseArray= response.pretty_print().split("\n")
    # result_payload = json.loads(responseArray[len(responseArray) - 2])
    
    client.stop()
    client.close()
    return result_good
