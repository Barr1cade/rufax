import re
import os
import zeep
import base64
import hashlib
from dotenv import load_dotenv

load_dotenv()

# Authentication
login = os.getenv('my_login')
password = os.getenv('my_password')
url = 'http://ws.rufax.ru/export/ws.rufax.ru/gws_01.wsdl'

client = zeep.Client(url)

# Получение идентификатора сессии
response = client.service.login(login=login, password=password)

# Extracting session ID from the response
session_id = response.sessionId

if not session_id:
    raise Exception('Not Found SessionId')

# Submit fax
file = 'fax.pdf'
with open(file, 'rb') as f:
    binary_data = f.read()
base64_binary = base64.b64encode(binary_data).decode('utf-8')
md5_hash = hashlib.md5(binary_data).hexdigest()

payload = {
    'recipient': os.getenv('my_number'),
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

# print(submit_fax_list_request)

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