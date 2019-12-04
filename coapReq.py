from coapthon.client.helperclient import HelperClient
import json, time

def message_to_json(message):
    message = json.dumps(message)
    return message
host = "148.213.190.187"
port = 5683


def getUser(pinCode):
    path ="/device/button"
    code = {
        "code": pinCode
    }
    payload = message_to_json(code)
    
    response = None
    result_good = {}
    client = None   
    try:
        time.sleep(2)
        print "\n\n\tIniciando Request con COAP..."
        client = HelperClient(server=(host, port))
        response = client.post(path,payload,None, timeout=5,)
        print response
        result_good['code'] = response.code
        result_good['payload'] = json.loads(response.payload)
    except:
        print "Something went wrong, try it againg!"
    # responseArray= response.pretty_print().split("\n")
    # result_payload = json.loads(responseArray[len(responseArray) - 2])
    
    client.stop()
    client.close()
    time.sleep(1)
    print"\n\n\t...All Good, request: \n\t\t" + str(result_good)
    return result_good
