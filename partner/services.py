import requests
from rest_framework.renderers import JSONRenderer
import json

def post_company_partners_type(username, data, password):
    url = 'https://wiconet-company-api.herokuapp.com/company_partnership_types/' 
    headers =  {'content-type' : 'application/json'}
    try: 
        r = requests.post(url, auth=('wiconet', 'w1c0net@app'), data=json.dumps(data), headers=headers)
        print(repr(r))
    except Exception as err :
        print(repr(err))

def post_company_partners(username, data, password):
    url = 'https://wiconet-company-api.herokuapp.com/company_partners/' 
    headers =  {'content-type' : 'application/json'}
    files = [
        ('image', open('/C:/Users/Anselme/Pictures/carte bancaire.jpg','rb'))
    ]
    try: 
        response = requests.post(url, auth=('wiconet', 'w1c0net@app'), data=data, headers=headers, files=files)
        print(repr(response))
    except Exception as error :
        print(repr(error))

    print(response.text.encode('utf8'))