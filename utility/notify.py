import requests
import json


serverToken = 'AAAAaIC2NFQ:APA91bFUn4sxpJJnaHAECR55PIe4C97lCF3GZGLe7ekq5s44sSN57lhDzWd7QYegi1l0nVk0dA47Cnh37WDRWnRhPavsCKVA7h3yy-lR2sghcNuuM-dqmJttFQEtX8ZWSZBgCeCqz9Al'
deviceToken = 'eGj79qVTS7iRx5X3x-07GQ:APA91bE94E2HTLuJ4hpfRGzKhtDc_W9k6TAPgMDMoyLznFTaxYIQdDUQBIv9dtZ9gu_Zrih0I9pDHtIIPT9WRyrG217uYIZJPz04eLmNFv-JDkz_gq23ID-t0ToHh9ZZDXnhNVBjz2LS'

headers = {
    'Content-Type':'application/json',
    'Authorization':'key='+serverToken
}
def notication(callObj):
    print(callObj)
    body = {
        'notication': {
        'title':'Call Arrived',
        'body':'new Call'
        },
        'to':deviceToken,
        'priority':'high'
    }
    response = requests.post("https://fcm.googleapis.com/fcm/send",headers = headers, data=json.dumps(body))
    print(response.status_code)
    print(response.json)
