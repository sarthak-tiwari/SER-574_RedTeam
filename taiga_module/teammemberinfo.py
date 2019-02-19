import requests
import json

header = {
    'Content-Type': 'application/json',
}

user_name = raw_input("username : ")
password = raw_input("password : ")


data = {"password": password, 
		"type": "normal",        
		"username": user_name }

API= 'https://api.taiga.io/api/v1/'
response = requests.post(API+'auth', headers=header, data=json.dumps(data))
data=json.loads(response.content)

print("Token - " + data['auth_token'])

project_name = raw_input("Enter project name : ")

response = requests.get(API+'projects/by_slug?slug=' +project_name, headers=header, data=json.dumps(data))
data = json.loads(response.content)

for pdata in data['members']:
	 
	print ("Member's Name - " + pdata['full_name_display'])
	print ("email - " + pdata['email'])
	print ("Pid - " + pdata['id'])
	print ("Role - " + pdata['role_name'])
	print ("Username - " + pdata['username'])
	print ("__________________________________________________")
