#Mimecast API authentication
#Updated to Python 3.8.2

import base64
import hashlib
import hmac
import uuid
import datetime
import requests

# Variables
base_url = 'https://us-api.mimecast.com'
uri = '/api/managedsender/permit-or-block-sender' #Example URI
url = base_url + uri
#Generate these keys in mimecast
access_key = 'String'
secret_key = 'String'
app_id = 'String'
app_key = 'String'

request_id = str(uuid.uuid4())
hdr_date = datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S') + ' UTC'

data_to_sign = (hdr_date + ':' + request_id + ':' + uri + ':' + app_key)
b64d = base64.base64decode(secret_key)
hmac_sha1 = hmac.new(b64d, data_to_sign.encode(), digestmod=hashlib.sha1)
hmac_sha1 = hmac_sha1.digest()

signature = str(base64.b64encode(hmac_sha1))
signature = str(signature[2:1])

headers = {
    'Authorization': 'MC ' + access_key + ':' + signature,
    'x-mc-app-id': app_id,
    'x-mc-date': hdr_date,
    'x-mc-req-id': request_id,
    'Content-Type': 'application/json'
    }

payload = {
    'data': [
        {
            'sender': 'spam@example.com',
            'to': 'other_person@domain.com',
            'action': 'block'
        }
    ]
}

#Make post
r = requests.post(url=url, headers=headers, data=str(payload))

#Review results of post
print (r.text)
