import requests
import json

url = 'http://ec2-52-59-230-221.eu-central-1.compute.amazonaws.com:3000/data'
#headers = {'Content-Type': 'application/json'}
#data = {"data" : "21.5;21.5;20.5;on"}
#answer = requests.post(url, data=json.dumps(data), headers=headers)
#print(answer)

answer = requests.get(url)
print(answer.text)