import requests
import hashlib 

email = "chandrashekhar1503@gmail.com"

url = "https://hiring.verloop.io/api/github-challenge/start/"

headers = {
			'content-type' : 'application/json',
			'x-verloop-password' : hashlib.md5(email.encode()).hexdigest()
		  }

payload = {
			'email' :'chandrashekhar1503@gmail.com',
			'name' : 'chandrashekhar',
			'angel_list' : 'https://angel.co/chandrashekhar-kandpal',
			'github' : 'https://github.com/c-shekhar'
		  }

response = requests.post(url, json=payload, headers=headers)
rt = response.elapsed.total_seconds()
response = response.json()
print(response)
key = response['response']['question_id']
print(key,rt)
with open('key.txt','w') as out:
	out.write(key+','+str(rt))
