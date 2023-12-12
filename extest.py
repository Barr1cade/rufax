"""
Аутентификация
"""
import re
import base64
import hashlib
import requests

login = 'login'
password = 'password'
url = 'http://ws.rufax.ru/export/ws.rufax.ru/gws_01.wsdl'

# Login
client = requests.Session()
response = client.get(url)
if response.status_code != 200:
    raise Exception('Failed to connect to the SOAP service')
session_id = re.search('<sessionId>([^<]+)</sessionId>', response.text)
if not session_id:
    raise Exception('Not Found SessionId')
session_id = session_id.group(1)

# Submit fax
file = 'fax.pdf'
with open(file, 'rb') as f:
    binary_data = f.read()
base64_binary = base64.b64encode(binary_data).decode('utf-8')
md5_hash = hashlib.md5(binary_data).hexdigest()

payload = {
    'recipient': '+74951234567',
    'attachment': {
        '_': base64_binary,
        'md5': md5_hash,
        'fileName': file
    },
    'act': 'send'
}

submit_fax_list_request = {
    'messageList': {
        'message': payload
    },
    'sessionId': session_id
}

response = client.post(url, json=submit_fax_list_request)
if response.status_code != 200:
    raise Exception('Failed to submit fax')
response_text = response.text

description = re.search('<description>([^<]+)</description>', response_text)
if description:
    description = description.group(1)
    description = description.encode('koi8').decode('utf-8')
else:
    description = ''

print(response_text)
print('\n\ndescription=' + description)

